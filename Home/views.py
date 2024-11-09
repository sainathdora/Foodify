from django.shortcuts import render
import tensorflow as tf
import os
import numpy as np
from PIL import Image
from django.core.files.storage import default_storage


tf.get_logger().setLevel('ERROR')

model_path = os.path.join('Home', 'model_EfficientNetb7(Augmentation)')
model = tf.keras.models.load_model(model_path)

food_items_macronutrients = {
    'adhirasam': {'protein': 1.5, 'carbohydrates': 35, 'fat': 4.0},
    'aloo_gobi': {'protein': 2.0, 'carbohydrates': 20, 'fat': 6.0},
    'aloo_matar': {'protein': 3.0, 'carbohydrates': 18, 'fat': 5.5},
    'aloo_methi': {'protein': 2.5, 'carbohydrates': 22, 'fat': 4.5},
    'aloo_shimla_mirch': {'protein': 2.0, 'carbohydrates': 23, 'fat': 4.0},
    'aloo_tikki': {'protein': 2.0, 'carbohydrates': 25, 'fat': 7.0},
    'anarsa': {'protein': 1.8, 'carbohydrates': 28, 'fat': 5.5},
    'ariselu': {'protein': 1.2, 'carbohydrates': 30, 'fat': 6.0},
    'bandar_laddu': {'protein': 3.5, 'carbohydrates': 40, 'fat': 8.0},
    'basundi': {'protein': 4.0, 'carbohydrates': 18, 'fat': 10.0},
    'bhatura': {'protein': 4.5, 'carbohydrates': 35, 'fat': 9.0}
}

food_items = [
    'adhirasam', 'aloo_gobi', 'aloo_matar', 'aloo_methi', 'aloo_shimla_mirch',
    'aloo_tikki', 'anarsa', 'ariselu', 'bandar_laddu', 'basundi', 'bhatura'
]

def display(request):
    return render(request, "Home/index.html", {'flag': False})


def upload_img(request):
    context = {'flag': False}  # Initialize context with flag set to False

    if request.method == 'POST' and request.FILES.get('image'):
        upload_image = request.FILES['image']
        print("uploaded image: ", upload_image)

        image = Image.open(upload_image).resize((224, 224))
        img_arr = np.array(image)  
        img_arr = np.expand_dims(img_arr, axis=0)
        
        # Make prediction
        pred1 = model.predict(img_arr)
       
        prediction = food_items[np.argmax(pred1)]
        probability = np.max(pred1)
        #  Update context with prediction results
        context.update({
            'flag': True,
            'probability': probability*100,
            'prediction': prediction,
            'nutrients': food_items_macronutrients[prediction],
        })
        
        # Render the template with the context and delete the image afterwards
    return render(request, 'Home/index.html', context)
