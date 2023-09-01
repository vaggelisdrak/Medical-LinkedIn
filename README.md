# A full stack web application like LinkedIn but for medical staff for a client

Most recent version climaxx-Copy (2)

I Created the backend of an existing website using Python's Flask. It inlcudes:

About the user:
  * A form in the main page where the user can search for a medical related job and filter based on the occupation, the specialty, the location (including autocomplete), keywords 
  * Search page in which the results are being fetched.Includes an advanced filtering system (salary per => hour/day/month/year, contract of length  => temporary/part-time/full) and a sorting system based on relevance, date posted (most recent job app) and salary comparison (ascending or descending order) 
  * Selected Options are saved into localstorage
  * Google Maps api => for each job application that satisfies the filtering options display data in a map using markers.Each marker includes some info about the job and a link that directs to the apply page 
  * If a user clicks the apply button, he is redirected to the apply page in which he can view more detalis ,fill a form with his data and CV, solve the reCAPTCHA and sumbit it
  * Confirmation email 
  * Featured jobs feature
  
About the recruiter-employer:
  * A register-login form + password hashing
  * password reset feature 
  * A dashboard where he can post a job ad ,edit or delete it (CRUD)
  * view the requests for each job ad he has made
  * Activate/Deactivate job ads (make them invisible)


Presentation

[Climax Resourcing.odp](https://github.com/vaggelisdrak/climaxx---medical-linkedin/files/11904316/Climax.Resourcing.odp)

Flowchart

![image](https://github.com/vaggelisdrak/climaxx---medical-linkedin/assets/71725114/382d037f-d1bb-45f4-96c7-6f8ba6dc1e2b)

Demo
