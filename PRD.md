# Self-aware researcher PRD


## 1 Main behaviors

* (core) Be able to connect to Sanity API and create new blog post data; 
* On-going research: specific scientific journals publications in order to find relevant publications aligned with the focus topics defined in a separate document called "areas of interest and scope" creating a report from abstract on potential blog articles to publish;
* Research the archives: scout my local Obsidian repository to find relevant articles or documents OR notes that I've written that would be interesting to write a blog post about aligned with the "areas of interest and scope" document;
* Execute: the custom built app might just prompt context (scientific articles) and the workflow will have to prepare and post (after supervision) a blog post on Sanity;

## 2 Triggers and running

1. It runs locally in npm instance from terminal;
2. It will have a custom coded app that interacts with it for user-in-the-loop nodes; (see "no name" app section)

## 3 "No name yet" App specifics

### 3.1 General overview

* It will be coded in Pyside;
* It will have a normal window UI and a minimized icon tray option which will be the bread and butter when the user is doing other work or working in tandem;
* It should be probably installable AND updatable through gitHub (if possible I upload a new version to git hub and the app automatically updates or at leasts prompts the user to update);


### 4 Execute

1. First step is to check if the provided context doesn't exceed the context window for and API request; the API key and llm model are defined in the Prompt Definition option in the main_workspace.py;
2. Second step is to take into account a reference document that gives a broad overview of compliancy on how to write the output article;
3. First attempt into writing the article; this requires most likely a specifically engineered prompt;
4. First draft is written send it back to the user through the API with the custom app; (Doable in Pyside?) the custom app has a built in editor; this built in editor allows to open read and modify the draft; the user modified parts take extreme priority and are then set as not modifiable by the n8n agent/workflow; the user can also just approve without reading to speed things up;
5. Proof read: the workflow through another API call will proof read the output/post; this will be achieved by following a careful set of instruction on a subsequent node; if the AI model proofreading the document thinks there's anything flagging, it sends another API call to the custom App that with the details, wich will allow the user to again use the editor to check the critical parts, modify it, or just read and approve it; 
6. Make another API call to the custom app for the user approval on publishing;
7. Permission is given, then API call to Sanity and publishing the blog post;


