# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from gluon import utils as gluon_utils
import json
import time

def index():
    pet_id = gluon_utils.web2py_uuid()
    return dict(pet_id=pet_id)

def load_pets():
    qset = db()
    qset = qset(db.pets.id > 0)
    pet_dict = qset.select()
    time.sleep(2)
    return response.json(dict(pet_dict=pet_dict))

def load_pets_initial():
    if session.pet_results == None:
        qset = db()
        qset = qset(db.pets.id > 0)
        pet_dict = qset.select()
    else:
        pet_dict = session.pet_results
    return response.json(dict(pet_dict=pet_dict))

def pets():
    pet_list = db().select(db.pets.ALL)
    pet_id = request.args(0)
    pic = db(db.pets.pet_id).select().first().pet_image
    return dict(pet_list=pet_list, pet_id=pet_id, pic=pic)

def get_pets():
    qset = db()
    user_selection = request.vars.get('user_selection[]') or request.vars.get('user_selection') or []
    if isinstance(user_selection, (str, unicode)):
        user_selection = [user_selection]

    for j in user_selection[0:]:
        if j == "house_trained": qset=qset(db.pets.house_trained == True)
        if j == "kid_friendly": qset=qset(db.pets.kid_friendly == True)
        if j == "indoor_pet": qset=qset(db.pets.indoor_pet == True)
        if j == "outdoor_pet": qset=qset(db.pets.outdoor_pet == True)
        if j == "frequent_exercise": qset=qset(db.pets.frequent_exercise)
        if j == "infrequent_exercise": qset=qset(db.pets.infrequent_exercise == True)
        if j == "young_pet": qset=qset(db.pets.young_pet == True)
        if j == "older_pet": qset=qset(db.pets.older_pet == True)
        if j == "pet_friendly": qset=qset(db.pets.pet_friendly == True)
        if j == "cat": qset=qset(db.pets.Cat_or_Dog == "Cat")
        if j == "dog": qset=qset(db.pets.Cat_or_Dog == "Dog")
        if j == "male": qset=qset(db.pets.gender == "Male")
        if j == "female": qset=qset(db.pets.gender == "Female")
        if j == "any_cat_dog": qset=qset(db.pets.Cat_or_Dog)
        if j == "any_gender": qset=qset(db.pets.gender)

    pet_dict = qset.select()
    session.pet_results = pet_dict
    time.sleep(2)
    return response.json(dict(pet_dict=pet_dict))

def addpet():
    form = SQLFORM(db.pets)
    if form.process().accepted:
       session.pet_results = None
       session.flash = 'A new pet has been added.'
       redirect(URL('index'))
    else:
       session.flash = 'Please fill out all that is necessary.'
    return dict(form=form)

@auth.requires_signature()
@auth.requires_login()
def delete():
    db(db.pets.id == int(request.args(0))).delete()
    redirect(URL('default', 'index'))
    session.flash = "Post Deleted"

@auth.requires_signature()
@auth.requires_login()
def edit():
    record = db.pets(request.args(0))
    edit_form = SQLFORM(db.pets, record=record)
    if edit_form.process().accepted:
        session.flash = "Post Edited"
        redirect(URL('default', index))
    return dict(edit_form=edit_form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
