"""
    Author: Brian Lam
    This file contains the classes and methods used to handle the intents for the Chamberlain Garage Door
    Opener skill. Note that this is an unofficial skill made by reverse engineering the API, and it may
    become obsolete with changes to Chamberlain's API. This file contains the lambda handler which is called for by
    AWS Lambda or an equivalent web service (as outlined by Amazon's requirements).
"""
import logging
import json
import garage_door_opener

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """
    This class is responsible for handling the launch of the Chamberlain Garage Door Opener skill.
    """
    def can_handle(self, handler_input):
        """
        Returns if the request type is LaunchRequest and invokes it with the handler_input.
        :param handler_input: the handler input
        :return: if the request type is LaunchRequest and invokes it with the handler_input
        """
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        """
        Given the handler input, login and generate the security token which is required for all garage door actions,
        and return to the user a message greeting them indicating the application has been launched.
        :param handler_input: the handler input which cause the launch request
        :return: a Response which contains a message greeting the user to the skill
        """
        speech_text = "Welcome to the Chamberlain Garage Door Opener!"
        with open("config.json") as config_file:
            config_contents = config_file.read()
            login_credentials = json.loads(config_contents)
            username = login_credentials["Username"]
            password = login_credentials["Password"]
            garage_door_opener.generate_security_token(username, password)

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Chamberlain Unofficial Garage Door Opener", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class CheckGarageDoorStateIntentHandler(AbstractRequestHandler):
    """
    This class is responsible for handling the checking of door state of the garage door.
    """
    def can_handle(self, handler_input):
        """
        Returns if the intent name is GarageDoorStateIntent and invokes the CheckGarageDoorStateIntent
        with the handler input.
        :param handler_input: the handler input
        :return: if the intent name is GarageDoorStateIntent and invokes the CheckGarageDoorStateIntent
        with the handler input.
        """
        return is_intent_name("CheckGarageDoorStateIntent")(handler_input)

    def handle(self, handler_input):
        """
        Returns a Response to the user about the garage door state.
        :param handler_input: the handler input
        :return: a Response of the garage door state
        """
        devices_endpoint = garage_door_opener.get_devices_endpoint()
        door_state = garage_door_opener.get_door_state(devices_endpoint)
        speech_text = "The garage door is " + door_state

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Garage Door State", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class OpenGarageDoorIntentHandler(AbstractRequestHandler):
    """
    This class is responsible for handling of opening the garage door.
    """
    def can_handle(self, handler_input):
        """
        Returns if the intent name is OpenGarageDoorIntent and invokes it with handler_input.
        :param handler_input: the handler input
        :return: if the intent name is OpenGarageDoorIntent and invokes it with handler_input
        """
        return is_intent_name("OpenGarageDoorIntent")(handler_input)

    def handle(self, handler_input):
        """
        Returns a Response with a message to the user about opening the garage door while opening the garage door.
        If the garage door is closed, it will indicate to the user the that garage door is opening.
        If it is already opened, it will indicate the garage door is already opened. If it is opening or closing,
        it will indicate it.
        :param handler_input: the handler input
        :return: a Response that indicates a message to the user about opening the garage door
        """
        devices_endpoint = garage_door_opener.get_devices_endpoint()
        door_message_number = garage_door_opener.do_door_action(devices_endpoint, "open")
        speech_text = garage_door_opener.DOOR_MESSAGES[door_message_number]
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Open Garage Door", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class CloseGarageDoorIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        """
        Returns if the intent name is CloseGarageDoorIntent and invokes it with handler_input.
        :param handler_input: the handler input
        :return: if the intent name is CloseGarageDoorIntent and invokes it with handler_input
        """
        return is_intent_name("CloseGarageDoorIntent")(handler_input)

    def handle(self, handler_input):
        """
        Returns a Response with a message to the user about closing the garage door while closing the garage door.
        If the garage door is opened, it will indicate to the user that the garage door is closing.
        If the garage door is already closed, it will indicate to the user that garage is already closed. If it is
        opening or closing, it will indicate it.
        :param handler_input: the handler input
        :return: a Response that indicates a message to the user about closing the garage door
        """
        devices_endpoint = garage_door_opener.get_devices_endpoint()
        door_message_number = garage_door_opener.do_door_action(devices_endpoint, "close")
        speech_text = garage_door_opener.DOOR_MESSAGES[door_message_number]
        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Close Garage Door", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """
    This class is responsible for handling help that the user may need with the skill.
    """
    def can_handle(self, handler_input):
    	"""
        Returns if the intent name is AMAZON.HelpIntent and invokes the AMAZON.HelpIntent with the handler input.
        :param handler_input: the handler input
        :return: if the intent name is AMAZON.HelpIntent and invokes the AMAZON.HelpIntent with the handler input
        """
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        """
        Return a Response to the user about what the skill can do.
        :param handler_input: the handler input
        :return: a Response to the user about what the skill can do
        """
        speech_text = "You can check the garage door status, and open or close the garage door"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Hello World", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """
    This class is responsible for handling of closing the garage door opener.
    """
    def can_handle(self, handler_input):
        """
        Returns if the intent name is AMAZON.CancelIntent or AMAZON.Stopintent and invokes it with the handler_input.
        :param handler_input: the handler input
        :return: if the intent name is AMAZON.CancelIntent or AMAZON.Stopintent and invokes it with the handler_input
        """
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        """
        Returns a Response to the user when the user closes the garage door opener.
        :param handler_input: the handler input
        :return: a Response to the user when the user closes the garage door opener
        """
        speech_text = "Goodbye!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Goodbye!", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """ AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "I can't help you with that. I can check the garage door status and open and close the garage " \
                      "door though."
        reprompt = "Try that out!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """ Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """ Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again later!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response


# Garage door specific handlers
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CheckGarageDoorStateIntentHandler())
sb.add_request_handler(OpenGarageDoorIntentHandler())
sb.add_request_handler(CloseGarageDoorIntentHandler())

# Required by Amazon's specifications
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
