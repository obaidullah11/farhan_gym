from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from .serializers import *





@api_view(['GET'])
def get_all_categories(request):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response({
            'success': True,
            'message': 'Categories retrieved successfully',
            'data': serializer.data
        }, status=200)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e),
            'data': []
        }, status=500)
@api_view(['GET', 'POST'])
def exercise_list_create(request):
    if request.method == 'GET':
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializernew(exercises, many=True)
        return Response({
            "success": True,
            "message": "Exercises retrieved successfully.",
            "data": serializer.data
        })

    elif request.method == 'POST':
        serializer = ExerciseSerializernew(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Exercise created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "message": "Exercise creation failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def exercise_detail(request, pk):
    try:
        exercise = Exercise.objects.get(pk=pk)
    except Exercise.DoesNotExist:
        return Response({
            "success": False,
            "message": "Exercise not found."
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExerciseSerializer(exercise)
        return Response({
            "success": True,
            "message": "Exercise retrieved successfully.",
            "data": serializer.data
        })

    elif request.method == 'PUT':
        serializer = ExerciseSerializer(exercise, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Exercise updated successfully.",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "message": "Exercise update failed.",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exercise.delete()
        return Response({
            "success": True,
            "message": "Exercise deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
# @api_view(['GET'])
# def routine_by_client(request, client_id):
#     try:
#         routines = Routine.objects.filter(client__id=client_id)

#         if not routines.exists():
#             return Response({
#                 "success": False,
#                 "message": "No routines found for this client."
#             }, status=status.HTTP_404_NOT_FOUND)

#         serializer = newRoutineSerializer(routines, many=True)
#         return Response({
#             "success": True,
#             "message": "Routines retrieved successfully.",
#             "data": serializer.data
#         }, status=status.HTTP_200_OK)

#     except Exception as e:
#         return Response({
#             "success": False,
#             "message": f"An error occurred: {str(e)}"
#         }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# @api_view(['GET', 'POST'])
# def routine_list_create(request):
#     if request.method == 'GET':
#         routines = Routine.objects.all()
#         serializer = RoutineSerializer(routines, many=True)
#         return Response({
#             "success": True,
#             "message": "Routines retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'POST':
#         serializer = RoutineSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Routine created successfully.",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "success": False,
#             "message": "Routine creation failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def routine_detail(request, pk):
#     try:
#         routine = Routine.objects.get(pk=pk)
#     except Routine.DoesNotExist:
#         return Response({
#             "success": False,
#             "message": "Routine not found."
#         }, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = RoutineSerializer(routine)
#         return Response({
#             "success": True,
#             "message": "Routine retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'PUT':
#         serializer = RoutineSerializer(routine, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Routine updated successfully.",
#                 "data": serializer.data
#             })
#         return Response({
#             "success": False,
#             "message": "Routine update failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         routine.delete()
#         return Response({
#             "success": True,
#             "message": "Routine deleted successfully."
#         }, status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def session_list_create(request):
#     if request.method == 'GET':
#         sessions = Session.objects.all()
#         serializer = SessionSerializer(sessions, many=True)
#         return Response({
#             "success": True,
#             "message": "Sessions retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'POST':
#         serializer = SessionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Session created successfully.",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "success": False,
#             "message": "Session creation failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def session_detail(request, pk):
#     try:
#         session = Session.objects.get(pk=pk)
#     except Session.DoesNotExist:
#         return Response({
#             "success": False,
#             "message": "Session not found."
#         }, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SessionSerializer(session)
#         return Response({
#             "success": True,
#             "message": "Session retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'PUT':
#         serializer = SessionSerializer(session, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Session updated successfully.",
#                 "data": serializer.data
#             })
#         return Response({
#             "success": False,
#             "message": "Session update failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         session.delete()
#         return Response({
#             "success": True,
#             "message": "Session deleted successfully."
#         }, status=status.HTTP_204_NO_CONTENT)

# # @api_view(['GET', 'POST'])
# # def setgroup_list_create(request):
# #     if request.method == 'GET':
# #         setgroups = Setgroup.objects.all()
# #         serializer = SetgroupSerializer(setgroups, many=True)
# #         return Response({
# #             "success": True,
# #             "message": "Setgroups retrieved successfully.",
# #             "data": serializer.data
# #         })

# #     elif request.method == 'POST':
# #         serializer = SetgroupSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response({
# #                 "success": True,
# #                 "message": "Setgroup created successfully.",
# #                 "data": serializer.data
# #             }, status=status.HTTP_201_CREATED)
# #         return Response({
# #             "success": False,
# #             "message": "Setgroup creation failed.",
# #             "data": serializer.errors
# #         }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def setgroup_detail(request, pk):
#     try:
#         setgroup = Setgroup.objects.get(pk=pk)
#     except Setgroup.DoesNotExist:
#         return Response({
#             "success": False,
#             "message": "Setgroup not found."
#         }, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SetgroupSerializer(setgroup)
#         return Response({
#             "success": True,
#             "message": "Setgroup retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'PUT':
#         serializer = SetgroupSerializer(setgroup, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Setgroup updated successfully.",
#                 "data": serializer.data
#             })
#         return Response({
#             "success": False,
#             "message": "Setgroup update failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         setgroup.delete()
#         return Response({
#             "success": True,
#             "message": "Setgroup deleted successfully."
#         }, status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET', 'POST'])
# def set_list_create(request):
#     if request.method == 'GET':
#         sets = Set.objects.all()
#         serializer = SetSerializer(sets, many=True)
#         return Response({
#             "success": True,
#             "message": "Sets retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'POST':
#         serializer = SetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Set created successfully.",
#                 "data": serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response({
#             "success": False,
#             "message": "Set creation failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT', 'DELETE'])
# def set_detail(request, pk):
#     try:
#         set_instance = Set.objects.get(pk=pk)
#     except Set.DoesNotExist:
#         return Response({
#             "success": False,
#             "message": "Set not found."
#         }, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SetSerializer(set_instance)
#         return Response({
#             "success": True,
#             "message": "Set retrieved successfully.",
#             "data": serializer.data
#         })

#     elif request.method == 'PUT':
#         serializer = SetSerializer(set_instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({
#                 "success": True,
#                 "message": "Set updated successfully.",
#                 "data": serializer.data
#             })
#         return Response({
#             "success": False,
#             "message": "Set update failed.",
#             "data": serializer.errors
#         }, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         set_instance.delete()
#         return Response({
#             "success": True,
#             "message": "Set deleted successfully."
#         }, status=status.HTTP_204_NO_CONTENT)


