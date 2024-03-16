from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt

from .models import Company, Employee, AssetLog, Asset
from .serializers import CompanySerializer, EmployeeSerializer, AssetSerializer, AssetLogSerializer


# Create your views here.

# for all Api


@api_view(['GET'])
def home(request):
    return Response({'status': True})


# all company Route
# get company


@api_view(['GET'])
def get_all_company(request):
    company = Company.objects.all()
    serializer = CompanySerializer(company, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })


# store company

@api_view(['POST'])
def store_company(request):
    data = request.data
    serializer = CompanySerializer(data=data)
    # check data validation
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 201,
            'data': serializer.data,
            'message': "data saved successfully"
        })
    # if data not valid
    return Response({
        'status': 400,
        'data': serializer.data,
        'message': "Something is Wrong"
    })


# all for Employee

# get all employee  by company id


@api_view(['GET'])
def get_all_employee(request, company_id):
    employee = Employee.objects.filter(company_id=company_id)
    serializer = EmployeeSerializer(employee, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })


# store Employee

@api_view(['POST'])
def store_employee(request):
    data = request.data
    serializer = EmployeeSerializer(data=data)
    # check data validation
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 201,
            'data': serializer.data,
            'message': "data saved successfully"
        })
    # if data not valid
    return Response({
        'status': 400,
        'data': serializer.data,
        'message': "Something is Wrong"
    })


# for all Asset


# get all asset by company id
@api_view(['GET'])
def get_all_asset(request, company_id):
    asset = Asset.objects.filter(company_id=company_id)
    serializer = AssetSerializer(asset, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })


# get all available asset
@api_view(['GET'])
def get_all_available_asset(request, company_id):
    asset = Asset.objects.filter(company_id=company_id, is_available=True)
    serializer = AssetSerializer(asset, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })



# store Asset

@api_view(['POST'])
def store_asset(request):
    data = request.data
    serializer = AssetSerializer(data=data)
    # check data validation
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 201,
            'data': serializer.data,
            'message': "data saved successfully"
        })
    # if data not valid
    return Response({
        'status': 400,
        'data': serializer.errors,
        'message': "Something is Wrong"
    })


# for all Asset


# get all asset by company id
@api_view(['GET'])
def get_all_asset_log(request, company_id):
    assetLog = AssetLog.objects.filter(employee__company_id=company_id)
    serializer = AssetLogSerializer(assetLog, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })


@api_view(['GET'])
def get_all_asset_log_by_employee(request, employee_id):
    assetLog = AssetLog.objects.filter(employee_id=employee_id)
    serializer = AssetLogSerializer(assetLog, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })


@api_view(['GET'])
def get_all_asset_log_by_asset(request, asset_id):
    assetLog = AssetLog.objects.filter(asset_id=asset_id)
    serializer = AssetLogSerializer(assetLog, many=True)
    return Response({
        'status': 200,
        'data': serializer.data,
    })



# store Asset

@api_view(['POST'])
def store_asset_log(request):
    data = request.data
    serializer = AssetLogSerializer(data=data)
    # check data validation
    if serializer.is_valid():
        # get asset by id
        asset_id = request.data.get('asset')
        asset = Asset.objects.get(id=asset_id)

        # check asset issued or not
        if asset.is_available:
            asset.is_available = False
            asset.save()
            serializer.save()
            return Response({
                'status': 201,
                'data': serializer.data,
                'message': "data saved successfully"
            })
        else:
            return Response({
                'status': 400,
                'data': serializer.data,
                'message': "Asset is not available"
            })

    # if data not valid
    return Response({
        'status': 400,
        'data': serializer.errors,
        'message': "Something is Wrong"
    })


# for returned_items
@csrf_exempt
@api_view(['PUT'])
def returned_asset(request, asset_log_id):
    asset_log = AssetLog.objects.get(id=asset_log_id)
    # get asset by id
    asset_id = asset_log.asset_id
    asset = Asset.objects.get(id=asset_id)

    # asset now available now, and its returned
    # update return_date and is_retunted flag in asset log
    # update asset o is_available true

    asset.is_available = True
    return_date = request.data.get('returned_date')
    asset_log.returned_date = return_date
    asset_log.is_returned = True

    asset.save()
    asset_log.save()

    return Response({
        'status': 200,
        'message': "Asset Returned Successfully"
    })
