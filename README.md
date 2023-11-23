# Cloudification
Python based AI-as-a-service cloud system using split learning platform.

The ultimate goal of this project is to be used as an experimental environment for any study related to split learning with Pytorch. 



## Use case

1. The server initially sets pretrained model and split point then runs ***server.py***. 

2. Clients runs ***client.py***. They first download client model from the server.

3. Clients input their own data to the client model to generate *smashed data* and send them to the server.

4. The server returns the prediction by feeding them into the server model. 

   - Updating model does not supported in this phase but should be implemented soon.

     ​


## Initial Phase Goal

1. Make a simple server-client application (Done)
2. Pytorch environment Setup (Done)
3. Write a simple code to generate a trained deep learning model (Done)
4. Implement model splitter
   * Currently, Pytorch does not support generalized splitting

