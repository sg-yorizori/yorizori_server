from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Steps, Unit, Ingredients
from .serializers import RecipeSerializer, StepSerializer, UnitSerializer, IngredientsSerializer

from rest_framework import status, generics
from django.db.models import Case, When, Q


class RecipeAllViewAPI(APIView): #특정 유저가 작성한 레시피 전체
    def get(self, request, id):
        recipe_List = Recipe.objects.filter(writer = id)
        serializers = RecipeSerializer(recipe_List, many=True)
        return Response(serializers.data)

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
            # disliked가 포함된 레시피 리스트 얻고 그걸 다시 제외!

            # 비건 레벨에 맞는 제외 ingrd 포함해서 아래 코드 수정하기(합쳐주기)
            # ex_ingrds
            ex_units = Unit.objects.filter(ingrd_id__in=request.data["disliked"])

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

                #print("list ", len(in_recipes))
                #print("set ", len(set(in_recipes)))
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

                #print(len(search_recipe_id_List))
                #print(len(ex_recipe_id_List))
                #print(len(search_recipe_id_List))
                output_id_List = [x for x in search_recipe_id_List if x not in ex_recipe_id_List]
                #print(output_id_List)

                """
                ordering = 'FIELD(`id`, %s)' % ','.join(str(id) for id in output_id_List)
                print(ordering)
                recipe_List = Recipe.objects.filter(id__in=[output_id_List]).extra(
                    select={'ordering': ordering}, order_by=('ordering',))
                """
                preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(output_id_List)])
                recipe_List = Recipe.objects.filter(pk__in=output_id_List).order_by(preserved)
                #recipe_List = (Recipe.objects.exclude(id__in=ex_recipe_id_List)).filter(id__in=search_recipe_id_List)



        serializers = RecipeSerializer(recipe_List, many=True)
        return Response(serializers.data)

class RecipeCreateAPI(APIView):
    def post(self, request):
        serializers = RecipeSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
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
        serializers = StepSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

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
        serializers = UnitSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status = status.HTTP_400_BAD_REQUEST)

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
        Unit_List = Unit.objects.filter(recipe_id = id)
        serializers = UnitSerializer(Unit_List, many=True)
        return Response(serializers.data)


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