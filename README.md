⚠ Import repository from : https://gitlab.iut-valence.fr/cellardr/project-web-s2

Web server for the project of Web development (M2105).

Framework used :  
* Bootstrap : [https://getbootstrap.com/](https://getbootstrap.com/)
* Font Awesome : [https://fontawesome.com/](https://fontawesome.com/)

Library used :
* Cherrypy : [https://github.com/cherrypy/cherrypy](https://github.com/cherrypy/cherrypy)
* Mako : [https://pypi.org/project/Mako/](https://pypi.org/project/Mako/)
* PyMySQL : [https://github.com/PyMySQL/PyMySQL/](https://github.com/PyMySQL/PyMySQL/)

Installation : 
1. Create ressource/py/settings.py
2. Copy and fill the require information :
```python
## -*- coding: utf-8 -*-
def getSettings():
    settings = {
        "db": {
            "address": "DB_ADDRESS",
            "database": "DB_NAME",
            "login": "DB_USERNAME",
            "password": "DB_PASSWORD"
        }
    }
    return settings
```
3. Import cellardr.sql in your database
4. Run server.py
