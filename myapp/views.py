from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item

class ItemAPIView(APIView):
    def post(self, request):
        operation = request.data.get('operation')

        # Create
        if operation == 'create':
            name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')

            if name and description and price:
                item = Item.objects.create(name=name, description=description, price=price)
                return Response({'message': 'Item created', 'item': {
                    'id': item.id,
                    'name': item.name,
                    'description': item.description,
                    'price': item.price,
                }}, status=status.HTTP_201_CREATED)
            return Response({'error': 'Missing fields'}, status=status.HTTP_400_BAD_REQUEST)

        # Read (all or single)
        elif operation == 'read':
            item_id = request.data.get('id')
            if item_id:
                try:
                    item = Item.objects.get(id=item_id)
                    return Response({'item': {
                        'id': item.id,
                        'name': item.name,
                        'description': item.description,
                        'price': item.price,
                    }}, status=status.HTTP_200_OK)
                except Item.DoesNotExist:
                    return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                items = Item.objects.all()
                items_data = [
                    {'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price}
                    for item in items
                ]
                return Response({'items': items_data}, status=status.HTTP_200_OK)

        # Update
        elif operation == 'update':
            item_id = request.data.get('id')
            name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')

            try:
                item = Item.objects.get(id=item_id)
                if name:
                    item.name = name
                if description:
                    item.description = description
                if price:
                    item.price = price
                item.save()
                return Response({'message': 'Item updated'}, status=status.HTTP_200_OK)
            except Item.DoesNotExist:
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        # Delete
        elif operation == 'delete':
            item_id = request.data.get('id')
            try:
                item = Item.objects.get(id=item_id)
                item.delete()
                return Response({'message': 'Item deleted'}, status=status.HTTP_200_OK)
            except Item.DoesNotExist:
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'error': 'Invalid operation'}, status=status.HTTP_400_BAD_REQUEST)
