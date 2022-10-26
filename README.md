# Personal_portfolio  
<b>!WIP!</b>  
[![HitCount](https://hits.dwyl.com/RSPersonal/Personal_portfolio.svg?style=flat-square)](http://hits.dwyl.com/RSPersonal/Personal_portfolio)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/dwyl/auth_plug/Elixir%20CI?label=build&style=flat-square)

https://r-sparenberg-portfolio.com/

Technogoly stack used:
<h6><b>BACKEND</b></h6>
<p align="left">
   <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg"
      alt="python" width="40" height="40"/> </a>
   <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg"
      alt="postgresql" width="40" height="40"/> </a>
   <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img
      src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40"
      height="40"/> </a>
</p>
<h6><b>FRONTEND</b></h6>
<p>
   <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg"
      alt="html5" width="40" height="40"/> </a>
   <a href="https://getbootstrap.com" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/bootstrap/bootstrap-plain-wordmark.svg"
      alt="bootstrap" width="40" height="40"/> </a>
   <a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg"
      alt="css3" width="40" height="40"/> </a>
   <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank"
      rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg"
      alt="javascript" width="40" height="40"/></a>
   <a href="https://www.chartjs.org" target="_blank" rel="noreferrer"><img
      src="https://www.chartjs.org/media/logo-title.svg" alt="chartjs" width="40"
      height="40"/> </a>
</p>
<h6><b>VERSION</b></h6>
<p>
   <a href="https://www.git.com" target="_blank" rel="noreferrer"> <img
      src="https://raw.githubusercontent.com/devicons/devicon/master/icons/git/git-original-wordmark.svg"
      alt="html5" width="40" height="40"/> </a>
</p>

Dependencies:
Check requirements.txt for dependencies.  

<b>Main goals for making this website:</b>
1. Learn python backend development for webpages
2. Learn to build an REST API and connect this REST API to the current website
3. Learn Postgresql
5. Learn to connect an external API which makes an external call and retreives data
6. Build a simple CRUD application (Stocktracker)
7. Build a webscraper to get real estate data
8. Build real estate valuation tool based on scraped data and user input

#### Architecture
![architecture drawio (6)](https://user-images.githubusercontent.com/74533741/195254311-2d265edb-057f-4b4f-aea4-628b4c4ff8a6.png)


<b>Future goals</b>  
1. Dockerize project and host in docker image    
2. PDF Creation for stocktracker   
3. Import CSV files in stocktracker  

<b>Site structure:</b>
1. Homepage  
2. API Projects & Scripts     
3. Database projects  
4. Website projects     
4. Contact/Info  


<b>Homepage</b>  
Building the homepage was not that hard, but when i needed to integrate Postgresql, I hit a wall and could not figure out how to do it. After extensive searching and reading documentation I was able to create and connect the database both in production and locally. Next goals was to give the user the functionality to view the resume in both Dutch and English. 

<b>API Projects</b>  
Here I want to showcase that iam able to connect to an external API and retreive data to showcase on my page. 

<b>Database Projects</b>  
This is my main section to showcase projects like the stocktracker. I learned a lot from this section but mostly unittesting, catching exceptions, getting database instances, correct variable naming, connecting own REST api, connecting to external api etc. 

#### Database design for stocktracker

A user can have many portfolio's and a portfolio can have many positions.
<br/>
![Stocktracker design drawio (1)](https://user-images.githubusercontent.com/74533741/187614553-892c3e1e-c320-4895-8495-76a6ea0c82d4.png)


#### Notes

`gunicorn --worker-tmp-dir /dev/shm core.wsgi1` for gunicorn
`gunicorn core.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --worker-tmp-dir /dev/shm` for uvicorn
