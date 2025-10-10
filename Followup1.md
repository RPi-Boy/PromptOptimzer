I want you to first create a dev branch.

After that, I want you to make the following changes:
1. When I click the user icon in the top right corner, I want you to allow the user to enter another open router API key and then set it in the .env file and use it for the session.
2. When the user clicks on the i button of any output. I want it expand the card.
3. When the card is expanded, it should show the result, model name, and the time taken to generate the result, tokens used, and the prompt tokens used.
4. There should be a cross button to close this expanded view.
5. The models that can be selected shows only some of the models on openrouter. Also, on reload all the models change. I want it to be such that either all available models are shown, or there are 20 pre selected models shown. You can see all the available model on the Openrouter website. If you decide to have a fixed set of models. I want you to make it so that there is a static model_list file in the models folder. This should contain selected models. If you decide to show all models, then the model_list file should be empty.

I want you to beautify the website also. Make a dark theme and make it responsive. Let there be a gradient background with very very subtle animations. 
Make sure all the text fields are safe. No sql query can be injected. No xss attacks can be done. 
Make sure the website is fast and responsive. 

When all this is done. I want you to make a dockerfile so it is easy to deploy. Only make the docker file no need to build it just yet.