# I3-RA : Raxter-PublicationClassifier

The user is able to upload a .pdf file that will be assigned 3 different concepts: Core, Peripheral, and Other.
The file will be parsed and split into smaller phrases to be designated their descriptions based on how relevant the phrase is to the main topic of the .pdf text.

Relevancy of the phrases is determined by a network with input layer size 1024, 2 dense hidden layers also 1024. Output is size 3 with softmax activation.

![Screenshot](https://i.imgur.com/ZVACR1r.png)<br/>
<br/>

The model searches for the highest used n-grams inside the .pdf text and  stores them into a list for future use. LDA (Latent Dirichlet allocation) is used to seperate the .pdf text into three distinct groups of words unsupervised (topics) and saved..

![Screenshot](https://i.imgur.com/XAK09ri.png)<br/>
<br/>

 The top n-grams are searched for and are now word embedded, using a word2vac model from pdfs, and put into a vector, the same embedding is done to the three topics previously created by the LDA
 
 ![Screenshot](https://i.imgur.com/CA74LnU.png)<br/>
 <br/>
 
 
 The data will all put into a Model object which calculates classification using its member functions.
 ![Screenshot](https://i.imgur.com/XIqUQJp.png)
 

 
The results are returned to the user on the screen and is then able to judge by a "Accept/Reject" of their opionion of the classification. The user input is recieved as a True and False and entered into a list. The user input list is compared to the predicted list using the resulting output to count the false positives, true negatives, true positives, as well as the calcilate accuracy based on the user's judgment.
