**An agent-based simulation to study the effect of vaccines on COVID-19 transmission**

**Project Ideas**
- analyze the effect of vaccines on the spread of COVID-19 
- Compare the spread/ death rates before and after vaccine implementations 
- Predict the rate of COVD- spread over the next few years

  
**Summary**

The primary objective of this project is to analyze the effect of vaccines on COVID-19 transmission using an agent-based simulation. 

For the construction of agent-based model, a simulation was developed to emulate the contraction of COVID-19 within a high school environment. The key variables incorporated into the simulation model include unvaccinated, vaccinated, and infected individuals. The construction of this model drew inspiration from the ABM Butterflies and Wallflower starter code, which served as the foundation for simulating the interactions among individuals.

To maintain simplicity within the model, certain assumptions were made, which include:  individuals being unaware of the virus and the inexistence of COVID protocols such as mask-wearing, maintaining a distance of 6 feet, and operating within small populations and rooms. being 6 feet apart, being in a small population in rooms, etc. These assumptions were strategically introduced to facilitate random movements for both infected and non-infected individuals, without alterations in response to the presence of the virus. 


Data pertaining to high school vaccination rates and the probabilities associated with contracting or transmitting the virus were sourced for the simulation. According to a survey conducted by Inside Higher Ed, vaccination rates among high school students in the United States range from 50% to 75%. Additionally, insights from a journal article in The Lancet indicate that the probability of a vaccinated individual contracting COVID-19 stands at 25%, whereas the probability for an unvaccinated individual is reported to be 38%.


**Model Explanation and Results**

In the implemented Agent-Based Simulation, the simulation scenario involves the dynamic movement of 60 students, resembling a classroom setting. Each student operates under the assumption of being unaware of their COVID-19 status. Consequently, the mobility patterns of infected students, unvaccinated students (yet uninfected), and vaccinated students (yet uninfected) are entirely stochastic. The initiation of the simulation involves the inclusion of six students who have already contracted the infection.

When a non-infected student is a close contact (within one unit of infected student), their risk of contracting Covid is dependent on their vaccination status. For unvaccinated individuals, we found significant research to conclude that — on average — the likelihood of contracting COVID-19 in close contact settings ranged from 20% to 26%. Conversely, for vaccinated individuals, research indicated an average likelihood falling within the range of 5% to 10.7%. Thus, if a student is a close contact, their probability of contracting COVID-19 is drawn from a Uniform distribution, employing the infection percentage ranges as bounds. 

![Screenshot (553)](https://github.com/carolynchep/covidtransmission/assets/152312583/f7334b07-018d-4ba3-8b09-c490b03507f9)

With this model, we successfully implemented exponential interarrivals to simulate the rate at which unprotected and vaccinated individuals contracted  COVID-19. We also incorporated a recovery time parameter, set at approximately t=10. This recovery time represents the duration within which individuals, upon being infected, undergo the process of recovery. 


**Future Studies**

The outcomes of this simulation reveal that unvaccinated students exhibited an approximately 10% higher likelihood of contracting COVID-19 when exposed via close contact, compared to their vaccinated counterparts. These results lead us to the conclusion that the administration of the vaccine significantly diminishes the probability of contracting COVID-19 in close contact settings.

In our future study, we plan to conduct a comprehensive comparison and introduce additional agents or factors that influence the number of infections at any given time. Among the factors under consideration are the immunity probability, representing the likelihood of individuals getting infected again, and the death probability. The model could also be expanded to show the rates of transmission depending on the number of vaccinated individuals who have received one or two boosters.
By incorporating these variables into our model, we anticipate to gain a more nuanced understanding of their impact on the dynamics of infection rates.



**Reference:**

➢ Redden, Elizabeth. “Survey: 50% of Students Attend Colleges with Vaccine Mandate.” Inside 
Higher Ed | Higher Education News, Events and Jobs. Accessed April 19, 2023.
https://www.insidehighered.com/quicktakes/2021/11/17/survey-50-students-attend-colleges-vacci ne-mandate. 

➢ “Community Transmission and Viral Load Kinetics of the SARS ... - the Lancet.” Accessed April 19, 2023. https://www.thelancet.com/journals/laninf/article/PIIS1473-3099(21)00648-4/fulltext. ➢ “Frontiers | Simulation Agent-Based Model to Demonstrate the ...” Accessed April 19, 2023. https://www.frontiersin.org/articles/10.3389/fcomp.2021.642321/full. 

➢ Faucher, Benjamin, Rania Assab, Jonathan Roux, Daniel Levy-Bruhl, Cécile Tran Kiem, Simon Cauchemez, Laura Zanetti, Vittoria Colizza, Pierre-Yves Boëlle, and Chiara Poletto. “Agent-Based Modelling of Reactive Vaccination of Workplaces and Schools against Covid-19.” Nature News. Nature Publishing Group, March 17, 2022. 
https://www.nature.com/articles/s41467-022-29015-y. 

➢ Va ́zquez-Abad Felisa J., and Daniel DufresneIMPACT OF VACCINATION POLICIES FOR COVID-19 USING HYBRID SIMULATION. “INFORMS-Sim.org.” IMPACT OF VACCINATION POLICIES FOR COVID-19 USING HYBRID SIMULATION. Accessed April 19, 2023. https://informs-sim.org/wsc22papers/049.pdf.
