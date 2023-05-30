# Managerial Incentives and Collusive Outcomes in Duopoly

This repository contains the oTree code for an experimental study that examines the impact of managerial incentives, specifically Relative Performance Evaluation (RPE), on collusive outcomes in a quantity-setting duopoly.

## Introduction

The purpose of this research project is to investigate how managerial incentives, particularly Relative Performance Evaluation (RPE), influence collusive outcomes in a duopoly scenario. The oTree code provided in this repository enables the implementation of the experimental study. The relevant app name is CournotSupergame.

## Pages Summary

1. **General Introduction to the Lab**: 
   - This page provides a general introduction to the experimental lab, explaining the purpose and goals of the study. It sets the context for the participants and provides lab specific instructions.

2. **Market Environment Introduction**: 
   - This page introduces the participants to the market environment in which they will be operating. It provides information about the market structure, remunration of each contract (one that contains RPE bonus (contract B) and one that is based solely on the Absolute Performance (Contract A)).

3. **Calculator Introduction**: 
   - This page presents the participants with a calculator tool. The calculator allows them to input different decision variables and calculate their potential profit and compensation outcomes based on the decisions they and other participants make. It serves as a valuable tool for participants to analyze and strategize their choices.
   - Participants can use sliders on the calculator page to change the quantity setting and immediately see the profits of both companies and their own payoff.
   - The calculator page also includes comprehension questions about how the calculator and contracts work. Participants must answer these questions correctly to proceed further in the experiment.

4. **Supergames Introduction**: 
   - This page provides detailed information about the supergames within the experiment. It explains the concept of supergames, including the stopping probability, which determines the duration of each supergame. Participants learn about the rules and dynamics of the supergames they will encounter during the experiment.
   - The participants can also play a mock game against themselves to better understand how they will be remunerated. 

5. **New Supergame Page**: 
   - This page serves as a transition point between supergames. Participants are matched with other participants based on predetermined matching configurations. The availability of this page depends on the treatment specified in the session configs. If the treatment allows for chatting, participants have the option to engage in a 180-second chat session before each supergame.

6. **Payoff-Relevant Decision Making**: 
   - After the participants are matched and the chat session has ended, they engage in payoff-relevant decision making round by round. On each page they get the information about their contract, contract of the participant they are matched with, calculator and past history (with this participant). 
   - The number of rounds is not fixed and participants do not know how many rounds they will play. However, they will at _minimum_ 10 rounds. If the random draw determines that they the market ends before 10 rounds (say the random draw results n<10 rounds), then only the first n rounds will be relevant for payoff. 
   - After a supergame is finished (i.e. max\[10,n] rounds are played), they will be transfered to the "New Supegame page" 

7. **Questionnaire for the University of Wuppertal**: 
   - This optional page presents a questionnaire for participants to provide information to the University of Wuppertal. The purpose is to anonymize potential participants and link them to existing studies. This option can be turned on/off based on the session configs.

8. **Final Results Page**: 
   - This page randomly selects one supergame out of the four and provides the output of decisions made by participants. It calculates the resulting payoffs based on the decisions and random draws for the round and displays the final results. Participants can see the outcome of their choices and analyze the impact of managerial incentives on collusive outcomes.

## Additional Notes

- The matching is hard-coded for a group of 16 participants. Therefore, if you are using rooms or a demo session, there should always be exactly 16 participants (otherwise there would be an error).
- There are two options for the duration of the supergame. If `pre_rolls` is set to `false` in the session configs, the rounds are not pre-rolled and are unknown to the participants and experimenter until each supergame starts. If `pre_rolls` is set to `true`, the rounds are pre-rolled but not known to the participants. In the latter case, the rolls happen when the session is created (potential problem with that is that rounds are very unbalanced: i.e. even though the expected number of rounds is 10 with 90% continuation probability, one can get a supergame that lasts for 40-50 rounds. Thus, we advice to do pre_rolls option which results in the durations of 11,8,13,9 rounds (to change that one can do pre rolls in any other software and then edit "\_init\_.py" file in the cournotsupergame folder.
-The experiment can be tested with bots - that select a value based on the tests.py file. 
## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use the code and adapt it for your own research purposes.
