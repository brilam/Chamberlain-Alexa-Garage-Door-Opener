# Chamberlain Alexa Unofficial Garage Door Opener
Control and monitor your garage door using Alexa. You can check the status of your garage door, and open and close the
garage door.

## License
This code is licensed under GNU GPL v3.0. See [here](https://github.com/brilam/Chamberlain-Alexa-Garage-Door-Opener/blob/master/LICENSE) for more details.

## Last Updated
This was last updated on December 24th 2018 and supports Chamberlain's v5.1 API. 

## Setting Up
Unfortunately, due to the skill being unofficial, I cannot publish to the Alexa Skill store. The only way this skill can
be used is via a developer account. You'll need to make a developer account with Amazon and you'll need either AWS
Lambda or a web service that adheres to Amazon's requirements which can be found [here](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-a-web-service.html)

Setting this up is similar to setting up any other Alexa skill as a developer. I would recommend that you check [this](https://github.com/alexa/skill-sample-python-helloworld-classes/blob/master/instructions/1-voice-user-interface.md) 
from Amazon. Here are some notes that are particular to this skill:

1) Instead of using the Hello World skill, you will be uploading [this zip file](https://github.com/brilam/Chamberlain-Alexa-Garage-Door-Opener/releases/tag/v1.0) to AWS Lambda. There is a config.json located 
in the zip file. This is where you include your Chamberlain login credentials. 

2) You will be using the JSON in the models/ folder for your Alexa Skill in the Alexa Developer Console. 
You can replace this JSON directly under JSON editor.

## Usage
Using the garage door opener skill is easy!

Just say Open garage door opener to open the skill. From there, you can do one of the following:

1. Is the garage door open?
2. Is the garage door closed?
3. Check the status of the garage door.
4. Open the garage door.
5. Close the garage door.

It is as simple as that!

**NOTE: I would highly recommend setting Alexa to only recognize certain voices in your household. See [this](https://www.amazon.com/gp/help/customer/display.html?nodeId=202199330) for more details.**

## Contributions & Issues
Issues are inevitable and this is bound to happen considering I've only tested this with my own garage door. 
Contributions are always welcome, and I encourage any issue reports to be submitted. I am also willing to 
look into feature requests as well.

## Disclaimer
This is an unofficial Alexa skill for Chamberlain's Garage Door which was created by reverse engineering the API, and this
skill could possibly be broken anytime due to API changes. I will try my best to keep the code updated. Also note that the author 
doesn't claim responsibility for any damages whatsoever, and created this project for educational purposes 

