$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});
$(function () {
    $('[data-toggle="popover"]').popover()
});
function requestAPI(type, link, html_id){
    $.ajax({
        dataType: "html",
        method: type,
        url: link,
        cache: false
    })
    .done(function( html ) {
        $( "#"+html_id ).html(html);
    }).fail(function() {
        html = `<div class="alert alert-danger p-3 m-3"><i class="fas fa-exclamation-circle"></i> Erreur avec la page... Veuillez réessayez plus tard :(</div>`;
        $( "#"+html_id ).html(html);
    });
}
function showBoxContent(str) {
    var html_id = "boiteContent";
    if (str == "") {
        $("#"+html_id).innerHTML = "Erreur dans l'affichage des informations de la boite";
        return;
    }
    requestAPI("GET", "api/boiteInfo?id="+str, html_id);
}
function srcBoite(type = null){
    var name= "",age= "",theme= "",sort = $('#btnSort').val(),html_id,url = "";
    html_id = "listBoites";
    if ($('#categorieAge').val() != "age"){
        age = $('#categorieAge').val();
    }
    if ($('#nomTheme').val() != "theme"){
        theme = $('#nomTheme').val();
    }
    if (type == "alphabet"){
        if($('#btnSort').hasClass('fa-sort-alpha-up')){
            $('#btnSort').removeClass('fa-sort-alpha-up').addClass('fa-sort-alpha-down');
            $('#btnSort').val("down");
            
        } else {
            $('#btnSort').removeClass('fa-sort-alpha-down').addClass('fa-sort-alpha-up');
            $('#btnSort').val("up");
        }
    }
    name = $('#search_boite_nom').val();
    sort = $('#btnSort').val();
    url = `api/srcBoite?name=${name}&age=${age}&themeID=${theme}&sort=${sort}`;
    requestAPI("GET", url, html_id);

}
function srcBriques(type = null){
    var taille="", couleur="", url="";
    var html_id = "listBriques";
    if ($('#couleur').val() != "couleur"){
        couleur = $('#couleur').val();
    }
    if (type == "prix"){
        if($('#btnPrix').hasClass('fa-sort-up')){
            $('#btnPrix').removeClass('fa-sort-up').addClass('fa-sort-down');
            $('#btnPrix').val("down");
        } else {
            $('#btnPrix').removeClass('fa-sort-down').addClass('fa-sort-up');
            $('#btnPrix').val("up");
        }
    }
    url = `api/srcBriques?couleur=${couleur}&sortPrix=${$('#btnPrix').val()}`;
    if($("#boiteID").val() != undefined){
        url += "&boiteID="+$("#boiteID").val();
    }
    requestAPI("GET", url, html_id);
}
function getListElement(){
    var cat = "", html_id = "listElement", url;
    if ($("#selectCategory").val() != "categorie"){
        url = "api/getListElementSelect?cat="+$("#selectCategory").val()+"&idSelect="+html_id;
        requestAPI("GET", url, html_id);
        $("#"+html_id).show();
        $("#btnGo").show();
    } else {
        $("#"+html_id).hide();
        $("#btnGo").hide();
    }
}
function getTheListElement(){
    var html_id="listEditElement";
    if ($("#selectEditCategory").val() != "categorie"){
        url = "api/getListElementSelect?cat="+$("#selectEditCategory").val()+"&idSelect="+html_id;
        requestAPI("GET", url, html_id);
        $("#"+html_id).show();
        $("#btnEditGo").show();
    }
}
function srcEditPage(){
    var html_id = "editBoxForm";
    if ($("#elementListing_listEditElement").val() != "element"){
        url = "api/srcEditPage?cat="+$("#selectEditCategory").val()+"&idInfo="+$("#elementListing_listEditElement").val();
        requestAPI("GET", url, html_id);
    }
}
$("input[name='choixAction']").click(function(){
    var radioValue = $("input[name='choixAction']:checked").val();
    if(radioValue){
        switch(radioValue){
            case 'delete':
                $("#deleteBox").show(1000);
                $("#editBox").hide();
                $("#addBox").hide();
                break;
            case 'edit':
                $("#deleteBox").hide();
                $("#editBox").show(1000);
                $("#addBox").hide();
                break;
            case 'add':
                $("#deleteBox").hide();
                $("#editBox").hide();
                $("#addBox").show(1000);
                break;
            default :
                $("#deleteBox").hide();
                $("#editBox").hide();
                $("#addBox").hide();
                break;
        }  
    }
});
function runDelete(){
    table = $("#selectCategory").val();
    id = $("#elementListing_listElement").val();
    sqlDelete(table, id);
}
function addBricktoBox(){
    if ($("#elementListing_boxInfoFullScreen").val() == "element"){
        return alert("Veuillez mettre une brique !");
    }
    if ($("#quantiteBriques").val() == 0 || $("#quantiteBriques").val() == undefined){
        return alert("Veuillez mettre un nombre de brique !");
    }
    url = `api/addBrickToBox?idB=${$("#boiteID").val()}&idP=${$("#elementListing_boxInfoFullScreen").val()}&nb=${$("#quantiteBriques").val()}`;
    sqlInsert(url);
}
function addBrick(){
    if ($("#nomBriques").val() == undefined || $("#nomBriques").val() == ""){
        return alert("Veuillez mettre un nom de brique !");
    }
    if ($("#addCouleur").val() == "couleur"){
        return alert("Veuillez mettre une couleur !");
    }
    if ($("#addTaille").val() == "Taille"){
        return alert("Veuillez mettre une taille !");
    }
    if ($("#prixBriques").val() == 0 || $("#prixBriques").val() == undefined){
        return alert("Veuillez mettre un prix pour la brique !");
    }
    url = `api/addBrick?nom=${$("#nomBriques").val()}&idC=${$("#addCouleur").val()}&idT=${$("#addTaille").val()}&prix=${$("#prixBriques").val()}`;
    sqlInsert(url);
}
function runAdd(){
    if ($("#selectCategoryAdd").val() == "categorie"){
        return alert("Veuillez choisir une catégorie");
    }
    if ($("#elementName").val() == undefined || $("#elementName").val() == ""){
        return alert("Veuillez mettre un nom !");
    }
    if ($("#elementImgUrl").val() == undefined || $("#elementImgUrl").val() == ""){
        return alert("Veuillez mettre une URL vers une image !");
    }
    if ($("#elementDescription").val() == undefined || $("#elementDescription").val() == ""){
        return alert("Veuillez mettre une description !");
    }
    url = `api/addBoiteTheme?tbl=${$("#selectCategoryAdd").val()}&nom=${$("#elementName").val()}&urlImg=${$("#elementImgUrl").val()}&desc=${$("#elementDescription").val()}`;
    if($("#selectCategoryAdd").val() == "boite"){
        if ($("#elementTheme").val() == "theme"){
            return alert("Veuillez choisir un thème");
        }
        if ($("#elementAge").val() == "age"){
            return alert("Veuillez choisir une trnche d'âge");
        }
        url+= `&themeId=${$("#elementTheme").val()}&catAge=${$("#elementAge").val()}`;
    }
    sqlInsert(url);
}
function runAddEdit(){
    if ($("#edit_elementName").val() == undefined || $("#edit_elementName").val() == ""){
        return alert("Veuillez mettre un nom !");
    }
    if ($("#elementListing_listEditElement") == undefined || $("#elementListing_listEditElement") == ""){
        return alert("Veuillez choisir un élément à modifier");
    }
    if ($("#edit_elementImgUrl").val() == undefined || $("#edit_elementImgUrl").val() == ""){
        return alert("Veuillez mettre une URL vers une image !");
    }
    if ($("#edit_elementDescription").val() == undefined || $("#edit_elementDescription").val() == ""){
        return alert("Veuillez mettre une description !");
    }
    url = `api/EditBoiteTheme?tbl=${$("#selectEditCategory").val()}&nom=${$("#edit_elementName").val()}&urlImg=${$("#edit_elementImgUrl").val()}&desc=${$("#edit_elementDescription").val()}&infoID=${$("#elementListing_listEditElement").val()}`;
    if($("#selectEditCategory").val() == "boite"){
        if ($("#edit_elementTheme").val() == "theme"){
            return alert("Veuillez choisir un thème");
        }
        if ($("#edit_elementAge").val() == "age"){
            return alert("Veuillez choisir une trnche d'âge");
        }
        url+= `&themeId=${$("#edit_elementTheme").val()}&catAge=${$("#edit_elementAge").val()}`;
    }
    sqlUpdate(url);
}
function sqlDelete(table=null, id=null, id2=null){
    link = `api/sqlDelete?tb=${table}&id=${id}`;
    if(id2 != null){
        link += `&ids=${id2}`;
    }
    $.ajax({
        dataType: "html",
        method: "GET",
        url: link,
        cache: false
    })
    .done(function() {
        alert("Elément supprimé (pensez à rafraichir la page).");
    }).fail(function() {
        alert("Erreur lors de la supprission. veuillez réessayez plus tard...");
    });
}

function sqlInsert(link){
    $.ajax({
        dataType: "html",
        method: "GET",
        url: link,
        cache: false
    })
    .done(function() {
        alert("Elément ajouté (pensez à rafraichir la page).");
    }).fail(function() {
        alert("Erreur lors de l'ajout (doublons ou problème technique ?). veuillez réessayez plus tard...");
    });
}

function sqlUpdate(link){
    $.ajax({
        dataType: "html",
        method: "GET",
        url: link,
        cache: false
    })
    .done(function() {
        alert("Elément mis à jour (pensez à rafraichir la page).");
    }).fail(function() {
        alert("Erreur lors de la mise à jour (doublons ou problème technique ?). veuillez réessayez plus tard...");
    });
}