from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Steps, Unit, Ingredients
from .serializers import RecipeSerializer, StepSerializer, UnitSerializer, IngredientsSerializer
from django.contrib.auth.models import User

from rest_framework import status, generics
from django.db.models import Case, When, Q
from config.settings import *
from recipe.detect_ingrd.views_detect import *



class RecipeAllViewAPI(APIView): #특정 유저가 작성한 레시피 전체
    def get(self, request, id):
        recipe_List = Recipe.objects.filter(writer = id)
        serializers = RecipeSerializer(recipe_List, many=True)
        return Response(serializers.data)

def ex_ingrds(v, disliked):
    vegan = []
    if v>=1: vegan += [357, 356, 335, 329, 325, 306, 285, 279, 271, 268, 264, 243, \
                       237, 229, 228, 185, 152, 150, 137, 112, 102, 83, 80, 76, 69,\
                       65, 56, 21]
    if v>=2: vegan += [362, 336, 265, 261, 255, 226, 168, 89, 71, 58, 39]
    if v>=3: vegan += [350, 332, 324, 320, 318, 311, 298, 296, 281, 278, 277, 275,\
                       274, 270, 267, 253, 244, 240, 232, 224, 206, 198, 194, 187,\
                       178, 174, 161, 156, 149, 148, 145, 139, 134, 128, 86, 82,  \
                       44, 10]
    if v==4: vegan += [121, 52]
    elif v==5: vegan += [304, 301, 259, 251, 217, 208, 119, 116, 115, 103, 99, 97, \
                       95, 93, 64, 63, 55, 46, 31, 30, 6]
    if v==6: vegan += [121, 52, 304, 301, 259, 251, 217, 208, 119, 116, 115, 103,\
                       99, 97, 95, 93, 64, 63, 55, 46, 31, 30, 6]

    return list(set(vegan + disliked))

class RecipeListViewAPI(APIView):
    def get(self, request, id):
        recipe_List = Recipe.objects.filter(writer = id)
        serializers = RecipeSerializer(recipe_List, many=True)
        return Response(serializers.data)

    def post(self, request):
        flag = request.data["flag"]
        if (flag==1):
            recipe_List = Recipe.objects.filter(id__in = request.data["recipe_list"])

        elif (flag >= 2):
            ex_units = Unit.objects.filter(ingrd_id__in=ex_ingrds(request.data["vegan"], request.data["disliked"]))

            ex_recipes = []
            for unit in ex_units:
                ex_recipes.append(unit.recipe_id)

            ex_recipe_id_List = []
            for recipe in ex_recipes:
                ex_recipe_id_List.append(recipe.id)

            if flag==2:
                recipe_List = (Recipe.objects.exclude(id__in=ex_recipe_id_List)).order_by("-views")
                recipe_List = recipe_List[:10]
            elif flag==3:
                recipe_List = (Recipe.objects.exclude(id__in=ex_recipe_id_List)).order_by("-created_date")
                recipe_List = recipe_List[:10]
            else: #검색
                #재료 문자열 리스트를 재료 인스턴스 리스트형으로
                ingrd = (request.data["search"]).split()
                ingrd_instance_List = Ingredients.objects.filter(name__in=ingrd)

                ingrd_List=[]
                for instance in ingrd_instance_List:
                    ingrd_List.append(instance.id)
                    #print(instance.name, instance.id)

                #검색할 재료를 유닛에서 검색. (12)당근 2개, (13)당근 1개, (12)양파1개
                in_units = Unit.objects.filter(ingrd_id__in=ingrd_List)

                in_recipes = []
                for unit in in_units:
                    in_recipes.append(unit.recipe_id)
                #일치하는 재료 개수만큼 레시피 추가됨

                count = {}
                for i in in_recipes:
                    try:
                        count[i] += 1
                    except:
                        count[i] = 1
                #print(sorted(count.items(), key=lambda item: item[1], reverse=True))
                sorted_count = sorted(count.items(), key=lambda item: item[1], reverse=True)
                #print(sorted_count)
                #겹치는게 많은걸 먼저 솔팅해서 id int list 추출하기

                search_recipe_id_List = []
                for recipe in sorted_count:
                    search_recipe_id_List.append(recipe[0].id)

                output_id_List = [x for x in search_recipe_id_List if x not in ex_recipe_id_List]

                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(output_id_List)])
                recipe_List = Recipe.objects.filter(pk__in=output_id_List).order_by(preserved)

        serializers = RecipeSerializer(recipe_List, many=True)
        return Response(serializers.data)

class RecipeCreateAPI(APIView):
    def post(self, request):
        d = Recipe.objects.create(
            title=request.data['title'],
            writer=User.objects.get(id=request.data['writer'])
        )

        recipe_id = Recipe.objects.latest('id').id
        if not os.path.exists(RECIPE_ROOT):
            os.makedirs(RECIPE_ROOT)
        if not os.path.exists(RECIPE_ROOT + "/" + str(recipe_id)):
            os.makedirs(RECIPE_ROOT + "/" + str(recipe_id))

        try:
            base64Image = request.data['thumb']
            base64Image = encodebase64(base64Image)

            thumb_url = MEDIA_URL + 'recipe/'+str(recipe_id)+"/"+"thumbnail.jpg"
            thumb_path = os.path.join(RECIPE_ROOT+"/"+str(recipe_id)+"/", "thumbnail.jpg")
            request.data['thumb'] = FRONT_HOST + thumb_url
            cv2.imwrite(thumb_path, base64Image)

            recipe = Recipe.objects.latest('id')

            serializers = RecipeSerializer(recipe, data=request.data)

            if serializers.is_valid():
               serializers.save()
               return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

        except:
            serializers = RecipeSerializer(d, data=request.data)
            if serializers.is_valid():
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

class RecipeDetails(APIView):
    def get_object(self, id):
        try:
            return Recipe.objects.get(id=id)

        except Recipe.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        recipe = self.get_object(id)
        serializers = RecipeSerializer(recipe)
        return Response(serializers.data)

    def put(self, request, id):
        recipe = self.get_object(id)
        serializers = RecipeSerializer(recipe, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        recipe = self.get_object(id)
        recipe.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



class StepsCreateAPI(APIView):
    def post(self, request):
        flag = 0
        for step in request.data:
            try :
                base64Image = step['img']
                base64Image = encodebase64(base64Image)

                step_path = os.path.join(RECIPE_ROOT, (str(step["recipe_id"])+"/"+str(step["num"])+".jpg"))
                step_url = MEDIA_URL + 'recipe/' + (str(step["recipe_id"])+"/"+str(step["num"])+".jpg")
                step['img'] = FRONT_HOST + step_url
                cv2.imwrite(step_path, base64Image)
                serializers = StepSerializer(data=step)

            except:
                serializers = StepSerializer(data=step)

            if serializers.is_valid():
                serializers.save()
            else:
                flag=1

        if flag==1 : Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)





class StepsAPI(APIView):
    def get_object(self, id):
        try:
            return Steps.objects.get(id=id)

        except Steps.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        Step = self.get_object(id)
        serializers = StepSerializer(Step)
        return Response(serializers.data)

    def put(self, request, id):
        Step = self.get_object(id)
        serializers = StepSerializer(Step, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        Step = self.get_object(id)
        Step.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class StepsAllViewAPI(APIView):
    def get(self, request, id):
        Step_List = Steps.objects.filter(recipe_id = id).order_by("num")
        serializers = StepSerializer(Step_List, many=True)
        return Response(serializers.data)


class UnitCreateAPI(APIView):
    def post(self, request):
        flag = 0
        for unit in request.data:
            ingrd = Ingredients.objects.get(name = unit["ingrd_id"])
            unit["ingrd_id"] = ingrd.id
            serializers = UnitSerializer(data=unit)

            if serializers.is_valid():
                serializers.save()
            else:
                flag=1
        if flag==1 : return Response(status = status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)



class UnitAPI(APIView):
    def get_object(self, id):
        try:
            return Unit.objects.get(id=id)

        except Unit.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        Unit = self.get_object(id)
        serializers = UnitSerializer(Unit)
        return Response(serializers.data)

    def put(self, request, id):
        Unit = self.get_object(id)
        serializers = UnitSerializer(Unit, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        Unit = self.get_object(id)
        Unit.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class UnitAllViewAPI(APIView):
    def get(self, request, id):
        Unit_before_List = Unit.objects.filter(recipe_id = id)
        Unit_List = []
        for raw in Unit_before_List:
            unit = UnitSerializer(raw).data
            ingrd = Ingredients.objects.get(id = unit["ingrd_id"])
            del unit["id"]
            del unit["ingrd_id"]
            del unit["recipe_id"]
            unit["ingrd_name"] = ingrd.name
            Unit_List.append(unit)
        return Response(Unit_List)


class IngrdCreateAPI(APIView):
    def post(self, request):
        serializers = IngredientsSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

class IngrdAPI(APIView):
    def get_object(self, id):
        try:
            return Ingredients.objects.get(id=id)
        except Ingredients.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        Ingredients = self.get_object(id)
        serializers = IngredientsSerializer(Ingredients)
        return Response(serializers.data)

    def put(self, request, id):
        Ingredients = self.get_object(id)
        serializers = IngredientsSerializer(Ingredients, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        Ingredients = self.get_object(id)
        Ingredients.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

#전체 리스트주는 get, ["당근", "사과", "오이"] 아니면 [1, 2, 3]
class IngrdAllViewAPI(APIView):
    def get(self, request):
        Ingredient_List = Ingredients.objects.all().order_by("name")
        serializers = IngredientsSerializer(Ingredient_List, many=True)
        return Response(serializers.data)

    def post(self, request):
        flag = request.data["flag"]
        if(flag==1): #["당근", "사과", "오이"]
            Ingredient_List = Ingredients.objects.filter(name__in = request.data["ingrd_List"])
            serializers = IngredientsSerializer(Ingredient_List, many=True)
        elif (flag == 2):  # [1, 2, 3]
            Ingredient_List = Ingredients.objects.filter(id__in=request.data["ingrd_List"])
            serializers = IngredientsSerializer(Ingredient_List, many=True)

        return Response(serializers.data)




# class RecipeView(APIView):
#     def get(self, request, **kwargs):
#         if kwargs.get('recipe_id') is None:
#             recipe_serializer = RecipeSerializer(
#                 Recipe.objects.all(), many=True)
#             return Response(recipe_serializer.data, status=200)
#         else:
#             recipe_id = kwargs.get('recipe_id')
#             recipe_serializer = RecipeSerializer(
#                 get_object_or_404(Recipe, id=recipe_id))
#             return Response(recipe_serializer.data, status=200)

"""
class IngredView(APIView):
    def get(self, request, **kwargs):
        if kwargs.get('ingred_id') is None:
            ingred_serializer = IngredSerializer(
                Ingred.objects.all(), many=True)
            return Response(ingred_serializer.data, status=200)
        else:
            ingred_id = kwargs.get('ingred_id')
            ingred_serializer = IngredSerializer(
                get_object_or_404(Ingred, id=ingred_id))
            return Response(ingred_serializer.data, status=200)
"""