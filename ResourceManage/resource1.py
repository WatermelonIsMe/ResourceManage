# encoding: utf-8
from flask import render_template, request, Response
from model import Resource_type, Details_applicants, Applicant, app, Resource_detail, db
import json


@app.route('/')
def index():
    return render_template('index.html')

#主界面，根据请求的服务器类型，返回对应的服务器详情和申请者的ip
@app.route('/resource_type/<int:type_id>/', methods=['GET'])
def get_resource_list(type_id):
    result = []
    resource_type_objs = Resource_type.query.filter_by(id=type_id).all()
    for resource_type_obj in resource_type_objs:
        tmp1 = Resource_detail.query.filter_by(type_Id=resource_type_obj.id).all()
        for item in tmp1:
            for _ in item.details_applicants:
                result.append(
                    {
                        # 'resource_detail_id': item.id,
                        # 'applicant_id': _.applicants.id,
                        'ip_address': item.ipaddress,
                        'application': item.application,

                            'ip_users': _.applicants.ip_users,

                    }
                )
    #返回json集合格式。
    return Response(json.dumps(result), content_type='application/json')





#查看详情，根据服务器ip查看申请者的详细信息
@app.route('/applicants/<string:ip_address>', methods=['GET'])
def get_resurce_detail_by_ip(ip_address):
    result = []
    resources = Resource_detail.query.filter_by(ipaddress=ip_address).all()
    for item in resources:
        for _ in item.details_applicants:
            result.append(
                {
                    'ip': _.applicants.ip_users,
                    'user_name': _.applicants.name,
                    'department': _.applicants.department,
                    'satffnumber': _.applicants.satffnumber,
                    'applytime': _.applicants.applytime,
                    'applyreason': _.applicants.applyreason,

                }
            )
    return Response(json.dumps(result), content_type='application/json')


@app.route('/resource/add_applicant', methods=['POST'])
def resource_add_applicant():
    applicant = Applicant()
    resource_detail = Resource_detail()
    resource_detail.ipaddress = request.form.get('service_ip')
    resource_detail.application = request.form.get('application')
    resource_detail.type_Id = request.form.get('type_Id')
    applicant.ip_users = request.form.get('ip_users')
    applicant.name = request.form.get('name')


    db.session.add(resource_detail)
    db.session.commit()
    resources = Resource_detail.query.filter_by(
        ipaddress=request.form.get('service_ip')).all()


    db.session.add(applicant)
    db.session.commit()
    for resource in resources:
        a = Details_applicants()
        a.applicants_id = applicant.id
        a.resource_details_id = resource.id
        db.session.add(a)
    db.session.add(applicant)
    db.session.commit()
    return Response(content_type='application/json')


@app.route('/resource_detail/<string:resource_ip>')
def get_detail(resource_ip):
    service_detail = Resource_detail.query.filter_by(ipaddress=resource_ip).first()
    service_type = service_detail.resource_types.name
    service_result = {}
    if service_detail:
        service_result.update(ipaddress=service_detail.ipaddress)
        service_result.update(service_type=service_type)
        service_result.update(application=service_detail.application)

    applicant = []

    for item in service_detail.details_applicants:
        applicant.append(
            {
                'ip_users': item.applicants.ip_users,
                'name': item.applicants.name
            }
        )
    return Response(json.dumps({'service': service_result, 'applicant': applicant}),
                    content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)
