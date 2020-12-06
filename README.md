## Final Project of Data Science and Machine Learning Course
## Purwadhika Startup and Coding School 2020
# Medical Appointment No Show Prediction

### Introduction
In the scope of the medical system, cancellation refers to patients who are aware that they cannot keep the appointment and inform the health care staff at least 24 hours before the scheduled appointment. Not to be used interchangeably with cancellation, the word ‘no show’ refers to patients who silently fail to attend a scheduled medical appointment. This term is further extended for those who cancel the appointment within 24 hours before the scheduled appointment.<br/>
Vitoria Apart Hospital is one of the biggest private healthcare industries in Brazil. It has four hospital branch around Vitoria, Espirito Santo State. As a big health care center, it can handle up to 80,000 medical appointment per month. Unfortunately, not all patients can keep up of their scheduled medical appointment. Approximately 20% of the medical appointment is a no-show case. 

### Problem Statement
High no show rate has been a catastrophic disaster for the business as it cost about BRL6,177,120 (USD1,153,718) from their monthly revenue.

### Goals
- Identifying the factors of no show behavior
- Finding quantitative measure that represent the factors
- Building machine learnng model to predict no show patients
- Connecting the prediction system into a dashboard

### Result
- Factors of no show behavior includes:
  1. Patient related issue (e.g: scared of the bad news the doctor will give, scared of the medical procedure)
  2. Environmental issue (e.g: transportation, colliding schedule between work and appoitment)
  3. Financial issue (e.g: afraid that they cannot afford the treatment cost)
  4. Scheduling related issue (e.g: patient was unclear about the schedule or appointment regulations)
- Quantitative measure that represents the factors:
  1. Age of patient
  2. Waiting time
  3. SMS reminder sent
  4. Status of holding Bolsa Familia
  5. Status of suffering hypertension
  6. Status of suffering diabetes
- Machine learning model:
  - The data was trained and tested using four machine learning model: logistic regression, KNN classifier, random forest classifier, and XGB classifier
  - Scoring of model was based on recall score and ROC score
  - Top models are random forest and XGB
  - After roughly calculating financial projection, it is found that random forest is more savvy (the calculation details is on pdf file)
- Dashboard
  - Dashboard menu consists of insights, data display, charts, and prediction
  - Healthcare frontier can see the prediction of a patient and the percentage they would keep the appoinment

### Recommendation
- The hospital can use random forest model to predict no show patient and save about BRL24 per appointment entry
- Recommended actions to handle no show suspect:
  1. Reminder (through SMS and call)
  2. Shorten the waiting time
  3. Enhance patient’s understanding about scheduling system and health care procedure they may experience

### Note
Although we handle all no show suspect, there is always possibility they miss the appointment. But, at least we have tried a way. Further study is needed to see the effectiveness of the recommendation above.