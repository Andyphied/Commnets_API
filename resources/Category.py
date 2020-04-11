from flask import request
from flask_restful import Resource
from Model import db, Category, CategorySchema


categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()

class CategoryResource(Resource):

    def get(self):
        categories = Category.query.all()
        categories = categories_schema.dump(categories).data
        return {'status': 'success', 'data': categories}, 200

    
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return ({'message': 'No input data provided'}, 400)
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return (errors, 422)
        category = Category.query.filter_by(name=data['name']).first()
        if category:
            return ({'message': 'Category already exists'}, 400)
        category = Category(
            name=json_data['name']
            )
        session = db.session
        try:
            session.add(category)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()


        
        result = category_schema.dump(category).data

        return ({ "status": 'success', 'data': result }, 201)


    def put(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return ({'message': 'No input data provided'}, 400)
        data, errors = category_schema.load(json_data)
        if errors:
            return (errors, 422)
        category = Category.query.filter_by(id=data['id']).first()
        if not category:
            return ({'message': 'Category does not exists'}, 400)
        session = db.session
        try:
            session.query(Category).update(Category.name :data['name'])
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()

        category = Category.query.filter_by(id=data['id'])
        result = category_schema.dump(category).data

        return ({ "status": 'success', 'data': result }, 204)



    
    def delete(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data, errors = category_schema.load(json_data)
        if errors:
            return errors, 422
        category = Category.query.filter_by(id=data['id'])

        session = db.session

        try:
            session.query(Category).filter_by(id=data['id']).\
                delete()
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
        
        result = category_schema.dump(category).data

        return ({ "status": 'success', 'data': result}, 204)





            

