import discord
from discord.ext import commands
import requests #sirve para hacer peticiones a la API de OpenAI
import random

from googletrans import Translator
translator = Translator()

import pyttsx3

# Configuración de la voz
voice_index = 0
voice_rate = 150
voice_volume = 0.8
decir_en_voz = True  # Variable para controlar si el bot debe hablar o no

def hablar(texto):
    if decir_en_voz == False:  # Solo hablar si la variable decir_en_voz es True
        return
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    engine.setProperty('rate', voice_rate)
    engine.setProperty('volume', voice_volume)
    engine.setProperty('voice', voices[voice_index].id)

    engine.say(texto)
    engine.runAndWait()
    engine.stop()

intents = discord.Intents.default() #para que el bot pueda leer los mensajes y reaccionar a ellos
intents.message_content = True #permite leer el contenido de los mensajes

bot = commands.Bot(command_prefix='!', intents=intents) #crea el bot con el prefijo "!" y los intents definidos
user_language="es"  # Idioma predeterminado del bot (español)


list_of_facts = [
    "La contaminación del aire es responsable de aproximadamente 7 millones de muertes prematuras cada año en todo el mundo.",
    "El plástico puede permanecer durante décadas o siglos en el medio ambiente, dependiendo de su tipo y de las condiciones.",
    "Cada año, grandes cantidades de plástico llegan a los océanos, donde pueden dañar a los animales marinos.",
    "La deforestación contribuye al cambio climático al liberar dióxido de carbono y reducir la cantidad de árboles que lo absorben.",
    "El transporte que utiliza combustibles fósiles es una fuente importante de emisiones de gases de efecto invernadero.",
    "El reciclaje ayuda a reducir la cantidad de residuos que terminan en vertederos y en el ambiente.",
    "El uso excesivo de pesticidas puede contaminar el suelo y el agua, afectando a distintas especies.",
    "La energía renovable, como la solar y la eólica, ayuda a reducir la dependencia de los combustibles fósiles.",
    "El cambio climático aumenta el riesgo de algunos fenómenos extremos, como las olas de calor y las lluvias intensas.",
    "La conservación del agua es esencial para garantizar su disponibilidad para las generaciones futuras.",

    # Contaminación y residuos
    "Las colillas de cigarrillos contienen materiales y sustancias que pueden contaminar el suelo y el agua.",
    "Las pilas y baterías no deben desecharse junto con los residuos comunes cuando existen sistemas de recolección especiales.",
    "Los residuos electrónicos pueden contener materiales peligrosos, pero también metales que pueden recuperarse mediante el reciclaje.",
    "Los microplásticos son pequeñas partículas de plástico que se han encontrado en océanos, suelos y numerosos organismos.",
    "La quema de basura al aire libre puede liberar gases y partículas perjudiciales para la salud.",
    "Reducir los productos descartables ayuda a disminuir la cantidad de residuos que generamos.",
    "Separar correctamente los residuos facilita el reciclaje de materiales como el papel, el vidrio y ciertos plásticos.",
    "El compostaje permite transformar muchos residuos orgánicos en un material útil para mejorar el suelo.",

    # Cambio climático y energía
    "El dióxido de carbono es uno de los principales gases de efecto invernadero emitidos por las actividades humanas.",
    "El efecto invernadero natural mantiene la Tierra a una temperatura adecuada para la vida, pero su intensificación provoca calentamiento global.",
    "La quema de carbón, petróleo y gas natural libera gases de efecto invernadero.",
    "Los edificios consumen energía para la iluminación, la calefacción, la refrigeración y el funcionamiento de sus aparatos.",
    "Apagar las luces cuando no son necesarias puede ayudar a reducir el consumo eléctrico.",
    "Los electrodomésticos eficientes pueden realizar tareas utilizando menos electricidad.",
    "El transporte público puede reducir las emisiones por pasajero cuando reemplaza viajes individuales en automóvil.",
    "Caminar o utilizar la bicicleta para trayectos cortos puede reducir el uso de combustibles y mejorar la salud.",
    "Las olas de calor pueden aumentar la demanda de electricidad debido al uso de ventiladores y sistemas de refrigeración.",
    "El calentamiento global contribuye al aumento del nivel del mar mediante la expansión del agua oceánica y la pérdida de hielo terrestre.",

    # Agua y océanos
    "Los océanos absorben gran parte del exceso de calor acumulado en el sistema climático.",
    "El océano también absorbe parte del dióxido de carbono emitido por las actividades humanas, lo que provoca su acidificación.",
    "Los derrames de petróleo pueden perjudicar a las aves, los peces y otros organismos marinos.",
    "Las aguas residuales sin tratamiento adecuado pueden contaminar ríos, lagos y mares.",
    "Cerrar la canilla mientras nos cepillamos los dientes puede evitar el desperdicio de agua.",
    "Las fugas de agua en los hogares pueden provocar pérdidas importantes si no se reparan.",
    "Los humedales ayudan a regular el agua, almacenar carbono y proporcionar hábitat a numerosas especies.",
    "Los manglares pueden proteger las costas frente a la erosión y almacenar grandes cantidades de carbono.",

    # Biodiversidad y naturaleza
    "Los bosques albergan una gran diversidad de plantas, animales, hongos y microorganismos.",
    "Las abejas y otros polinizadores ayudan a la reproducción de numerosas plantas, incluidos muchos cultivos alimentarios.",
    "La pérdida de hábitats es una de las principales amenazas para la biodiversidad mundial.",
    "Las especies invasoras pueden alterar los ecosistemas y competir con las especies nativas.",
    "Los árboles capturan dióxido de carbono durante su crecimiento y almacenan carbono en su biomasa.",
    "Los suelos sanos son fundamentales para la producción de alimentos, el almacenamiento de carbono y la conservación del agua.",
    "Los incendios forestales pueden destruir hábitats y liberar el carbono almacenado en la vegetación.",
    "Proteger las especies nativas ayuda a mantener el equilibrio y la diversidad de los ecosistemas.",

    # Hábitos sostenibles
    "Reutilizar objetos puede reducir la necesidad de fabricar productos nuevos y generar residuos.",
    "Comprar solamente los alimentos que necesitamos ayuda a disminuir el desperdicio alimentario.",
    "Los restos de frutas y verduras pueden aprovecharse para producir compost si se gestionan adecuadamente.",
    "Reparar un objeto puede prolongar su vida útil y evitar que se convierta prematuramente en un residuo.",
    "Utilizar bolsas reutilizables puede disminuir el consumo de bolsas descartables.",
    "Donar o intercambiar ropa en buen estado puede prolongar su uso y reducir residuos textiles.",
    "La producción de alimentos requiere recursos como agua, energía, suelo y transporte.",
    "Elegir productos duraderos puede ayudar a reducir el consumo de materiales y la generación de residuos.",

    # Argentina y el medio ambiente
    "Los humedales del Delta del Paraná albergan una gran diversidad de especies y ayudan a regular el agua.",
    "Los glaciares andinos son importantes reservas de agua dulce y pueden verse afectados por el calentamiento global.",
    "Los bosques nativos argentinos brindan hábitat a numerosas especies y ayudan a conservar los suelos.",
    "Los incendios en los humedales pueden afectar la calidad del aire, la biodiversidad y la salud de las personas.",
    "La separación de residuos y el compostaje son acciones que pueden ayudar a reducir los residuos enviados a disposición final.",
    "El cuidado de los ríos y arroyos contribuye a proteger los ecosistemas y las fuentes de agua.",
    
    "Los árboles ayudan a reducir la temperatura de las ciudades al proporcionar sombra.",
    "Los residuos electrónicos pueden contener materiales valiosos que se pueden recuperar mediante el reciclaje.",
    "La contaminación lumínica puede alterar los hábitos de animales nocturnos.",
    "Las bolsas plásticas pueden llegar al mar y ser confundidas con alimento por algunos animales.",
    "El compostaje transforma restos orgánicos, como cáscaras de frutas, en un material útil para el suelo.",
    "Los océanos absorben parte del dióxido de carbono de la atmósfera, pero esto aumenta su acidez.",
    "Las colillas de cigarrillo pueden liberar sustancias contaminantes cuando entran en contacto con el agua.",
    "Quemar basura puede liberar gases y partículas perjudiciales para la salud y el ambiente.",
    "El desperdicio de alimentos también desperdicia el agua y la energía utilizados para producirlos.",
    "Las pilas deben desecharse en puntos de recolección adecuados para evitar la liberación de sustancias peligrosas.",
    "Los neumáticos liberan pequeñas partículas al desgastarse, que pueden terminar en el suelo y el agua.",
    "El calentamiento del océano puede provocar el blanqueamiento de los corales.",
    "Los aparatos electrónicos viejos pueden reciclarse para recuperar materiales como cobre y aluminio.",
    "Los plásticos pueden fragmentarse en microplásticos sin desaparecer por completo del ambiente.",
    "El exceso de fertilizantes puede contaminar ríos y lagos y reducir el oxígeno disponible para los peces.",
    "Los incendios forestales pueden destruir hábitats y liberar grandes cantidades de humo y dióxido de carbono.",
    "La contaminación del aire puede viajar largas distancias y afectar lugares alejados de su origen.",
    "Las redes de pesca abandonadas pueden seguir atrapando animales marinos durante mucho tiempo.",
    "El reciclaje del aluminio suele consumir mucha menos energía que producir aluminio nuevo a partir de minerales.",
    "Los residuos orgánicos que se descomponen sin suficiente oxígeno pueden producir metano, un gas de efecto invernadero.",
    "Las tortugas marinas pueden confundir ciertos residuos plásticos con alimento.",
    "Apagar los aparatos eléctricos que no se utilizan ayuda a evitar el consumo innecesario de energía.",
    "La contaminación térmica ocurre cuando una actividad humana cambia la temperatura del agua y afecta a los organismos acuáticos.",
    "Reparar y reutilizar objetos ayuda a reducir la cantidad de residuos que generamos.",
    "Los océanos absorben gran parte del exceso de calor acumulado por el calentamiento global.",
    "Separar correctamente los residuos facilita su reciclaje y reduce la cantidad de basura que termina en vertederos.",
    
    # CAMBIO CLIMÁTICO Y ENERGÍA
    "El metano retiene mucho calor en la atmósfera y contribuye al calentamiento global.",
    "La quema de combustibles fósiles libera dióxido de carbono que puede permanecer en el sistema climático durante mucho tiempo.",
    "Las olas de calor pueden ser más intensas o frecuentes debido al cambio climático, aunque sus efectos varían según la región.",
    "El cambio climático puede modificar las temporadas de lluvia y aumentar el riesgo de sequías en algunas zonas.",
    "La energía hidroeléctrica utiliza el movimiento del agua para generar electricidad, pero las represas también pueden alterar los ecosistemas de los ríos.",
    "Los paneles solares pueden generar electricidad sin quemar combustibles durante su funcionamiento.",
    "Los vehículos eléctricos no producen gases de escape mientras circulan, aunque su impacto ambiental total depende de cómo se fabrican y de cómo se genera la electricidad.",
    "Mejorar la eficiencia energética permite obtener el mismo resultado utilizando menos energía.",
    "El aire acondicionado consume electricidad y puede aumentar la demanda energética durante los días de mucho calor.",
    "Los edificios con buen aislamiento pueden mantener mejor la temperatura interior y reducir el consumo de calefacción y refrigeración.",

    # RECICLAJE Y HÁBITOS SOSTENIBLES
    "Antes de reciclar un envase, conviene revisar las indicaciones locales y comprobar si debe estar vacío o limpio.",
    "Reutilizar un frasco de vidrio puede alargar su vida útil antes de que se convierta en un residuo.",
    "Las botellas reutilizables deben lavarse con regularidad para mantenerlas limpias.",
    "Reparar un dispositivo electrónico puede evitar que se convierta prematuramente en basura electrónica.",
    "No todos los plásticos se reciclan de la misma manera; el tipo de material y las instalaciones disponibles influyen en el proceso.",
]




@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}') #muestra en la consola que el bot está conectado




@bot.command()
async def start(ctx):
    await ctx.send("¡Hola! Soy tu asistente de discord. Puedes pedirme los comandos que tengo para ayudarte con el comando !ayuda.")
    hablar("¡Hola! Soy tu asistente de discord. Puedes pedirme los comandos que tengo para ayudarte con el comando !ayuda.")


@bot.command()
async def ayuda(ctx):
    await ctx.send("Estos son los comandos que tengo disponibles:\n **!ayuda** para obtener la lista de comandos disponibles.\n **!fact** para obtener un dato sobre el medio ambiente y contaminacion.\n **!start** para iniciar el bot y escuchar un mensaje de bienvenida.\n **!config** para ver comandos de configuracion del bot.\n **!language** <idioma> para cambiar el idioma de los mensajes del bot .")
    hablar("Estos son los comandos que tengo disponibles:")
    

@bot.command()
async def config(ctx):
    await ctx.send("Estas son las configuraciones que tengo disponibles: \n **!voz on** para activar la función de hablar.\n **!voz off** para desactivar la función de hablar.")
    hablar("Estas son las configuraciones que tengo disponibles:")


@bot.command()
async def voz(ctx, estado: str):
    global decir_en_voz
    if estado == "on":
        await ctx.send("La función de hablar ha sido activada.")
        decir_en_voz = True
        hablar("La función de hablar ha sido activada.")
    elif estado == "off":
        await ctx.send("La función de hablar ha sido desactivada.")
        decir_en_voz = False
        hablar("La función de hablar ha sido desactivada.")






@bot.command()
async def fact(ctx):
    fact = random.choice(list_of_facts)
    await ctx.send(fact)
    hablar(fact)

bot.run("Token")
