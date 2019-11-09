"""
server.py

Author : remi_cellard
Date : 24/05/2019

"""

import cherrypy,os
from mako.template import Template
from mako.lookup import TemplateLookup
from mydir import getCurrentDir
# ---------
# La ligne suivante permet d'exécuter ce script sous M$ (blabla)
# ---------
_curdir = getCurrentDir()
# ---------

# ---------
# Fichier de configuration avec les pramètres du site
# ---------
from ressource.py.settings import getSettings
my_settings = getSettings()
# ---------

# ---------
# Gestion de la communication avec la base de donnée
# ---------
from ressource.py.rcBD import RC_DB, RC_DB_CMD
myDB = RC_DB(my_settings)
myCMD = RC_DB_CMD()


myTemplatesDir = os.path.join(_curdir,'ressource/template')
myModulesDir = os.path.join(_curdir,'ressource/tmp/mako_modules')
mylookup = TemplateLookup(directories=[myTemplatesDir], module_directory=myModulesDir,output_encoding='utf-8',input_encoding='utf-8',encoding_errors='replace')

class Root:
    def __init__(self):
        self.api = Api()

    @cherrypy.expose
    def index(self):
        mytemplate = mylookup.get_template("page/accueil.html")
        return mytemplate.render()
    
    @cherrypy.expose
    def themes(self, sort = None):
        mytemplate = mylookup.get_template("page/themes.html") ## Charger le template
        cmd = myCMD.theme_cmd({"order":{"info": ["nom"], "sort": "ASC"}})
        if not sort is None:
            if sort == "down":
                cmd = myCMD.theme_cmd({"order":{"info": ["nom"], "sort": "DESC"}})
        listThemes = myDB.fa(cmd)
        return mytemplate.render(listThemes=listThemes, sort=sort)

    @cherrypy.expose
    def boites(self, theme_id=None, sort=None):
        mytemplate = mylookup.get_template("page/boites.html") ## Charger le template
        
        ## Liste des commandes SQL
        cmdTheme = myCMD.theme_cmd({"order":{"info": ["id"], "sort": "ASC"}, "specificSelect": "id, nom"})
        configSearch = {
            "order":{
                "info": ["boite.nom"],
                "sort": "ASC"
            },
            "join": {
                "table": "theme",
                "conditions": [
                    "theme.id=boite.theme"
                ]
            },
            "specificSelect": "boite.id AS boiteID, boite.nom AS boiteNom, theme.nom AS themeNom, boite.img_link"
        }
        if not theme_id is None:
            try:
                theme_id = int(theme_id)
                configSearch["where"] = "boite.theme={}".format(theme_id)
            except Exception as error:
                pass
        if not sort is None:
            if sort == "down":
                configSearch["order"]["sort"] = "DESC"
        cmdBoite = myCMD.boites_cmd(configSearch)

        ## Execution des commandes SQL
        listAge = myDB.fa("SELECT SUBSTRING(COLUMN_TYPE,5)FROM information_schema.COLUMNS WHERE TABLE_NAME='boite' AND COLUMN_NAME='categorie_age'")
        listBoites = myDB.fa(cmdBoite)
        listTheme = myDB.fa(cmdTheme)
        return mytemplate.render(listBoites=listBoites, listAge=listAge, listTheme=listTheme)
    
    @cherrypy.expose
    def briques(self):
        listBriques = myDB.fa("SELECT pieces.id, pieces.nom AS pieceNom, couleur.rgb, couleur.nom AS couleurNom, CONCAT(taille.longueur,'x',taille.largeur,'x',taille.hauteur) as Dimension, pieces.prix FROM pieces JOIN couleur ON couleur.ref_color = pieces.couleur JOIN taille ON taille.ref_size = pieces.taille")
        listCouleur = myDB.fa("SELECT ref_color, nom, rgb FROM couleur")
        listTaille = myDB.fa("SELECT * FROM taille")
        mytemplate = mylookup.get_template("page/briques.html") ## Charger le template
        return mytemplate.render(listBriques=listBriques, listCouleur=listCouleur,listTaille=listTaille, allBriques = None)

    @cherrypy.expose
    def gestion(self):
        cmd = myCMD.theme_cmd({"order":{"info": ["nom"], "sort": "ASC"}, "specificSelect": "id, nom"})
        listTheme = myDB.fa(cmd)
        listAge = myDB.fa("SELECT SUBSTRING(COLUMN_TYPE,5)FROM information_schema.COLUMNS WHERE TABLE_NAME='boite' AND COLUMN_NAME='categorie_age'")
        mytemplate = mylookup.get_template("page/gestion.html") ## Charger le template
        return mytemplate.render(listTheme=listTheme, listAge=listAge)

class Api:
    @cherrypy.expose
    def index(self,**kwargs):
        cherrypy.response.status = 404
        return "404"

    @cherrypy.expose
    def boiteInfo(self,**kwargs):
        apiDone = False
        response = {}
        if 'id' in kwargs:
            cmd = myCMD.boites_cmd({
                "order":{
                    "info": ["boite.nom"],
                    "sort": "ASC"
                },
                "where": "boite.id = {}".format(kwargs['id']),
                "join": {
                    "table": "theme",
                    "conditions": [
                        "theme.id=boite.theme"
                    ]
                },
                "limit": 1,
                "specificSelect": "boite.id,boite.nom AS boiteNom,boite.categorie_age,boite.img_link,boite.description,theme.nom AS themeNom"
            })
            response["boiteInfo"] = myDB.fa(cmd)
            if len(response["boiteInfo"]) == 1:
                apiDone = True
                response["templateRequest"] = "block/block-boite-info.html"
        if not apiDone:
            cherrypy.response.status = 404
            return "Not Found"
        response["listBriques"] = myDB.fa("SELECT pieces.id, pieces.nom AS pieceNom, couleur.rgb, couleur.nom AS couleurNom, CONCAT(taille.longueur,'x',taille.largeur,'x',taille.hauteur) as Dimension, pieces.prix, liste_brique.quantite, boite.id FROM pieces JOIN liste_brique ON liste_brique.piece_id = pieces.id JOIN boite ON boite.id = liste_brique.boite_id JOIN couleur ON couleur.ref_color = pieces.couleur JOIN taille ON taille.ref_size = pieces.taille WHERE boite.id = {} ORDER BY pieces.prix ASC;".format(kwargs['id']))
        response["listCouleur"] = myDB.fa("SELECT ref_color, nom, rgb FROM couleur")
        

        ## Slector add pieces
        cmd = "SELECT id, CONCAT(pieces.nom,' - ',couleur.nom,' - ',taille.longueur,'x',taille.largeur,'x',taille.hauteur,' - ',pieces.prix,'euros') AS info FROM pieces JOIN couleur ON couleur.ref_color = pieces.couleur JOIN taille ON taille.ref_size = pieces.taille ORDER BY id ASC;"
        listingAllBriques = myDB.fa(cmd)
        selectorPieces = mylookup.get_template("block/gestion/block-list-element.html")
        response["allBriques"] = selectorPieces.render(listing=listingAllBriques, idSelect="boxInfoFullScreen")

        mytemplate = mylookup.get_template("page/api/response.html")
        return mytemplate.render(r="boiteInfo", data=response)
    
    @cherrypy.expose
    def srcBoite(self, name=None, age=None, themeID=None, sort=None, **kwargs):
        startWhere = False
        apiDone = False
        response = {}
        configSearch = {
            "order":{
                "info": ["boite.nom"],
                "sort": "ASC"
            },
            "join": {
                "table": "theme",
                "conditions": [
                    "theme.id=boite.theme"
                ]
            },
            "specificSelect": "boite.id AS boiteID, boite.nom AS boiteNom, theme.nom AS themeNom, boite.img_link"
        }
        if not name == "": 
            configSearch["where"] = 'boite.nom LIKE \'%{uname}%\' '.format(uname=name)
            startWhere = True
        if not age == "": 
            if startWhere:
                configSearch["where"] += "AND boite.categorie_age = '{}' ".format(age)
            else:
                startWhere = True
                configSearch["where"] = "boite.categorie_age = '{}' ".format(str(age))
        if not themeID == "": 
            if startWhere:
                configSearch["where"] += "AND boite.theme = '{}' ".format(themeID)
            else:
                startWhere = True
                configSearch["where"] = "boite.theme = '{}' ".format(themeID)
        if not sort == "":
            if sort == "down":       
                configSearch["order"]["sort"] = "DESC"
        response["srcBoite"] = myDB.fa(myCMD.boites_cmd(configSearch))
        if len(response["srcBoite"]) > 0:
            apiDone = True
            response["templateRequest"] = "block/block-boite-display.html"
        else:
            return '<div class="alert alert-danger p-3 m-3"><i class="fas fa-exclamation-circle"></i> Aucun résultat avec vos critères de recherche</div>'
        if not apiDone:
            cherrypy.response.status = 404
            return "Not Found"
        mytemplate = mylookup.get_template(response["templateRequest"])
        return mytemplate.render(listBoites=response["srcBoite"])
    
    @cherrypy.expose
    def srcBriques(self, couleur=None,prix=None,sortPrix=None, **kwargs):
        needQuantite = False
        cmdboiteID_pt1 = ""
        cmdboiteID_pt2 = ""
        if "boiteID" in kwargs: 
            cmdboiteID_pt1 = ",liste_brique.quantite, boite.id AS boiteID"
            cmdboiteID_pt2 = "JOIN liste_brique ON liste_brique.piece_id = pieces.id JOIN boite ON boite.id = liste_brique.boite_id WHERE boite.id = {} ".format(kwargs['boiteID'])           
            needQuantite = True
        cmd = "SELECT pieces.id, pieces.nom AS pieceNom, couleur.rgb, couleur.nom AS couleurNom, CONCAT(taille.longueur,'x',taille.largeur,'x',taille.hauteur) as Dimension, pieces.prix{} FROM pieces JOIN couleur ON couleur.ref_color = pieces.couleur JOIN taille ON taille.ref_size = pieces.taille {}".format(cmdboiteID_pt1, cmdboiteID_pt2)
        if not couleur == "": 
            if "boiteID" in kwargs:
                cmd += 'AND pieces.couleur = {} '.format(couleur)
            else:
                cmd += 'WHERE pieces.couleur = {} '.format(couleur)
        if sortPrix == "down":
            cmd += "ORDER BY pieces.prix DESC"
        else:
            cmd += "ORDER BY pieces.prix ASC"
        reponse = myDB.fa(cmd+";")
        listCouleur = myDB.fa("SELECT ref_color, nom, rgb FROM couleur")

        ## Slector add pieces
        cmd = "SELECT id, CONCAT(pieces.nom,' - ',couleur.nom,' - ',taille.longueur,'x',taille.largeur,'x',taille.hauteur,' - ',pieces.prix,'euros') AS info FROM pieces JOIN couleur ON couleur.ref_color = pieces.couleur JOIN taille ON taille.ref_size = pieces.taille ORDER BY id ASC;"
        listingAllBriques = myDB.fa(cmd)
        selectorPieces = mylookup.get_template("block/gestion/block-list-element.html")
        allBriques = selectorPieces.render(listing=listingAllBriques)
        listTaille = myDB.fa("SELECT * FROM taille")
        mytemplate = mylookup.get_template("block/block-line-brique.html")
        return mytemplate.render(listBriques=reponse, listCouleur=listCouleur, listTaille=listTaille, needQuantite=needQuantite, allBriques=allBriques)

    @cherrypy.expose
    def getListElementSelect(self, cat=None, idSelect=None, **kwargs):
        if (cat is None) or (idSelect is None) or not (cat in ["theme", "boite"]) :
            return '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> Erreur de requête vers le serveur</div>'
        cmd = "SELECT id, nom FROM {} ORDER BY id ASC;".format(cat)
        listing = myDB.fa(cmd)       
        mytemplate = mylookup.get_template("block/gestion/block-list-element.html")
        return mytemplate.render(listing=listing, idSelect=idSelect)

    @cherrypy.expose
    def srcEditPage(self, cat=None,idInfo=None, **kwargs):
        if (idInfo is None) or (cat is None) or not (cat in ["theme", "boite"]) :
            return '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> Erreur de requête vers le serveur</div>'
        if cat == "boite":
            params = "id, nom, img_link, description, theme, categorie_age"
        else:
            params = "id, nom, img_link, description"
        cmd = "SELECT {} FROM {} WHERE id = {} ORDER BY id ASC;".format(params, cat, idInfo)
        listing = myDB.fa(cmd)
        if len(listing) == 0:
            return '<div class="alert alert-danger"><i class="fas fa-exclamation-circle"></i> aucun élément trouvé.</div>'
        cmd = myCMD.theme_cmd({"order":{"info": ["nom"], "sort": "ASC"}, "specificSelect": "id, nom"})
        listTheme = myDB.fa(cmd)
        listAge = myDB.fa("SELECT SUBSTRING(COLUMN_TYPE,5)FROM information_schema.COLUMNS WHERE TABLE_NAME='boite' AND COLUMN_NAME='categorie_age'")
        mytemplate = mylookup.get_template("block/gestion/block-edit-item.html")
        return mytemplate.render(listing=listing, listTheme=listTheme, listAge=listAge)

    @cherrypy.expose
    def sqlDelete(slef, tb=None, id=None, **kwargs):
        if (tb is None) or not (tb in ["theme", "boite", "pieces", "liste_brique"]) or (id is None):
            cherrypy.response.status = 409
            return "409"
        cmd = "DELETE FROM {} ".format(tb)
        if tb == "liste_brique":
            if not "ids" in kwargs:
                cherrypy.response.status = 409
                return "409"
            cmd += "WHERE boite_id = {} AND piece_id = {}".format(id, kwargs["ids"])
        else:
            cmd += "WHERE id = {}".format(id)
        myDB.exec(cmd)
        cherrypy.response.status = 202
        return "202"
    
    @cherrypy.expose
    def addBrickToBox(self, idB=None, idP=None, nb=None, **kwargs):
        if (idB is None) or (idP is None) or (nb is None):
            cherrypy.response.status = 409
            return "409"
        ## check if exist 
        cmd = "SELECT * FROM liste_brique WHERE boite_id = {} AND piece_id = {};".format(idB, idP)
        result = myDB.fa(cmd)
        if len(result) > 0:
            ancienneValeur = int(nb)+int(result[0][2])
            cmd = "UPDATE liste_brique SET quantite = {} WHERE boite_id = {} AND piece_id = {};".format(int(ancienneValeur),idB, idP)
        else:
            cmd = "INSERT INTO liste_brique (boite_id, piece_id, quantite) VALUES ({}, {}, {});".format(idB, idP, nb)
        myDB.exec(cmd)
        cherrypy.response.status = 202
        return "202"
    @cherrypy.expose
    def addBrick(self, nom=None, idC=None, idT=None, prix=None,**kwargs):
        if (nom is None) or (idC is None) or (idT is None) or (prix is None):
            cherrypy.response.status = 409
            return "409"
        cmd = "INSERT INTO pieces (nom, couleur, taille, prix) VALUES ('{}', {}, {}, {});".format(nom, idC, idT, prix)
        myDB.exec(cmd)
        cherrypy.response.status = 202
        return "202"
    @cherrypy.expose
    def addBoiteTheme(self, tbl=None, nom=None, urlImg=None, desc=None, **kwargs):
        if (nom is None) or (urlImg is None) or (desc is None) or (tbl is None) or not (tbl in ["theme", "boite"]):
            cherrypy.response.status = 409
            return "409"
        cmd = "INSERT INTO {} (nom, img_link, description) VALUES ('{}', '{}', '{}');".format(tbl, nom, urlImg, desc)
        if('themeId' in kwargs) and ('catAge' in kwargs):
            cmd = "INSERT INTO {} (nom, theme, categorie_age, img_link, description) VALUES ('{}', '{}', '{}', '{}', '{}');".format(tbl, nom, kwargs['themeId'], kwargs['catAge'], urlImg, desc)
        myDB.exec(cmd)
        cherrypy.response.status = 202
        return "202"
    @cherrypy.expose
    def EditBoiteTheme(self, tbl=None, nom=None, urlImg=None, desc=None, infoID=None, **kwargs):
        if (nom is None) or (urlImg is None) or (desc is None) or (tbl is None) or not (tbl in ["theme", "boite"]) or (infoID is None):
            cherrypy.response.status = 409
            return "409"
        cmd = "UPDATE {} SET nom='{}', img_link='{}', description=\"{}\" WHERE id = {};".format(tbl, nom, urlImg, desc, infoID)
        if('themeId' in kwargs) and ('catAge' in kwargs):
            cmd = "UPDATE {} SET nom='{}', img_link='{}', description=\"{}\", theme='{}', categorie_age='{}' WHERE id = {};".format(tbl, nom, urlImg, desc, kwargs['themeId'], kwargs['catAge'], infoID)
        myDB.exec(cmd)
        cherrypy.response.status = 202
        return "202"

if __name__ == '__main__':
    print(_curdir)
    # La configuration n'est plus dans un fichier, mais directement ici!
    cherrypy.config.update({'server.socket_host' : "127.0.0.1", 
                            'server.socket_port' : 8080,
                            'server.protocol_version' : 'HTTP/1.1',
                             'tools.encode.encoding' : "Utf-8"})

    conf = {'/public': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(_curdir, 'ressource')},
            '/public/template': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': myTemplatesDir},
            '/public/tmp/mako_modules': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': myModulesDir},
            '/public/css': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(_curdir, 'ressource/css'),
                            'tools.staticdir.content_types': {'css': 'text/css'}},
            '/public/js': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(_curdir, 'ressource/js'),
                            'tools.staticdir.content_types': {'js': 'text/js'}},
            '/public/webfonts': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(_curdir, 'ressource/webfonts'),
                            'tools.staticdir.content_types': {'font': 'text/font'}},
            '/public/img': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(_curdir, 'ressource/img'),
                      }
            }
    cherrypy.quickstart(Root(), '/', config=conf)
