
import streamlit as st
import re

# =====================================================
# FARMASSIST - AGRICULTURAL ADVISORY CHATBOT
# =====================================================

st.set_page_config(
    page_title="FarmAssist",
    page_icon="🌱",
    layout="wide"
)

# ---------------- PROFESSIONAL DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #F5F8F3;
}

.main-title {
    color: #205C37;
    font-size: 42px;
    font-weight: bold;
}

.subtitle {
    color: #647568;
    font-size: 17px;
}

div.stButton > button {
    border-radius: 10px;
    border: 1px solid #B8CCB9;
    min-height: 43px;
}

div.stButton > button:hover {
    border-color: #267A42;
    color: #267A42;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- PAGE HEADER ----------------

st.markdown(
    '<div class="main-title">🌱 FarmAssist</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your Agricultural Advisory Chatbot</div>',
    unsafe_allow_html=True
)

st.write(
    "Welcome to FarmAssist! Ask questions about crop production, "
    "plant diseases, livestock, animal health, poultry, soil and irrigation."
)

st.divider()


# =====================================================
# FARMING KNOWLEDGE DATABASE
# =====================================================

RULES = [

    # -------------------------------------------------
    # 1. CROP PRODUCTION
    # -------------------------------------------------

    (
        r"\b(grow|plant|planting|growing)\b.*\b(tomato|tomatoes)\b|"
        r"\b(tomato|tomatoes)\b.*\b(grow|plant|planting)\b",

        """
### 🍅 Growing tomatoes

1. Choose a place that receives plenty of sunlight.
2. Prepare well-drained soil and add mature compost.
3. Plant healthy seedlings.
4. Leave enough space between plants.
5. Water regularly, especially during dry weather.
6. Support plants using stakes.
7. Check regularly for pests and diseases.

Avoid overwatering because it can damage the roots.
"""
    ),

    (
        r"\b(best time|when)\b.*\b(plant|planting)\b.*\b(maize|corn)\b|"
        r"\b(maize|corn)\b.*\b(planting season|plant)\b",

        """
### 🌽 Best time to plant maize

The best planting time depends on rainfall, temperature and your location.

1. In rain-fed farming, plant after reliable rains have started.
2. Prepare the land before the planting season.
3. Use suitable maize varieties for your area.
4. Avoid planting into very dry soil.
5. Ask your local agricultural extension officer about the recommended planting dates.

In Namibia, planting dates can differ between regions.
"""
    ),

    (
        r"\b(water|watering|often|irrigat)\b.*\b(cabbage|cabbages)\b|"
        r"\b(cabbage|cabbages)\b.*\b(water|watering|irrigat)\b",

        """
### 🥬 Watering cabbage

Cabbage needs regular water to grow properly.

1. Keep the soil consistently moist.
2. Check the soil before watering.
3. Water near the roots.
4. Increase attention during hot and dry weather.
5. Avoid waterlogging.
6. Use mulch to help keep moisture in the soil.

The amount of water depends on the weather, soil and growth stage.
"""
    ),

    (
        r"\b(yellow|yellowing)\b.*\b(leaves|leaf)\b.*\b(tomato|tomatoes)\b|"
        r"\b(tomato|tomatoes)\b.*\b(yellow|yellowing)\b",

        """
### 🍅 Yellow leaves on tomato plants

Possible causes include:

1. Too much water.
2. Too little water.
3. Lack of nutrients.
4. Root damage.
5. Plant diseases or pests.

What to do:

- Check whether the soil is too wet or too dry.
- Inspect the leaves for spots and insects.
- Check whether the plant is growing normally.
- Improve drainage if water collects around the roots.
- Ask an agricultural officer if the problem continues.

Yellow leaves alone cannot identify the exact problem.
"""
    ),

    (
        r"\b(soil|type of soil)\b.*\b(bean|beans)\b|"
        r"\b(bean|beans)\b.*\b(soil)\b",

        """
### 🫘 Suitable soil for beans

Beans generally grow well in fertile, well-drained soil.

Good soil should:

1. Allow water to drain properly.
2. Contain organic matter.
3. Have enough nutrients.
4. Not be too compacted.
5. Have a suitable soil pH.

Avoid planting in waterlogged soil because roots need air.
"""
    ),

    (
        r"\b(improve|increase|higher|better)\b.*\b(maize|corn)\b.*\b(production|yield|harvest)\b|"
        r"\b(maize|corn)\b.*\b(yield|production)\b",

        """
### 🌽 Improving maize production

1. Use healthy and suitable seeds.
2. Prepare the soil properly.
3. Plant at the recommended spacing.
4. Control weeds early.
5. Apply suitable fertiliser based on soil needs.
6. Provide enough water.
7. Monitor for pests and diseases.
8. Harvest at the correct maturity stage.

Good farming practices help improve production.
"""
    ),

    (
        r"\b(poor growth|not growing|slow growth|stunted)\b.*\b(vegetable|vegetables|plant|plants|crop|crops)\b|"
        r"\b(vegetable|vegetables|plant|plants|crop|crops)\b.*\b(poor growth|slow growth|stunted)\b",

        """
### 🌱 Poor growth in vegetable plants

Possible causes include:

1. Poor soil fertility.
2. Lack of water.
3. Too much water.
4. Poor sunlight.
5. Pests and diseases.
6. Poor soil drainage.
7. Incorrect planting spacing.

Check the soil, water supply, sunlight and leaves to identify possible problems.
"""
    ),

    (
        r"\b(prepare|preparing|preparation)\b.*\b(land|soil|field)\b.*\b(plant|planting)\b|"
        r"\b(land|soil|field)\b.*\b(before planting|prepare)\b",

        """
### 🚜 Preparing land before planting

1. Remove unwanted weeds.
2. Remove rubbish and unsuitable plant material.
3. Loosen the soil.
4. Break large soil clumps.
5. Add mature compost or suitable manure.
6. Prepare planting rows or beds.
7. Make sure water can drain properly.

Avoid working very wet soil because it can damage its structure.
"""
    ),

    (
        r"\b(why|what causes|cause)\b.*\b(tomato|tomatoes)\b.*\b(crack|cracking)\b|"
        r"\b(tomato|tomatoes)\b.*\b(crack|cracking)\b",

        """
### 🍅 Why tomatoes crack

Tomatoes can crack when they absorb water too quickly after a dry period.

Other factors include:

- Irregular watering.
- Heavy rainfall.
- Some variety differences.
- Temperature changes.

To reduce cracking:

1. Water regularly.
2. Avoid large changes in soil moisture.
3. Use mulch.
4. Choose suitable tomato varieties.
"""
    ),

    (
        r"\b(when|time)\b.*\b(harvest|harvesting)\b.*\b(onion|onions)\b|"
        r"\b(onion|onions)\b.*\b(harvest|ready)\b",

        """
### 🧅 When to harvest onions

Onions are generally ready when:

1. Their leaves begin turning yellow.
2. The tops start falling over naturally.
3. The bulbs have reached a suitable size.

After harvesting:

- Handle bulbs carefully.
- Allow them to dry in a well-ventilated place.
- Store in a cool, dry location.

Harvest timing also depends on the onion variety.
"""
    ),


    # -------------------------------------------------
    # 2. PLANT DISEASES AND PESTS
    # -------------------------------------------------

    (
        r"\b(fall armyworm|army worm)\b",

        """
### 🐛 Fall armyworm

Fall armyworm is an insect pest that mainly attacks maize and other crops.

Common signs include:

1. Holes in maize leaves.
2. Damage to young leaves.
3. Sawdust-like material inside the plant.
4. Damaged growing points.

Management:

- Inspect crops regularly.
- Identify the pest before choosing control methods.
- Remove affected plant material where practical.
- Ask an agricultural extension officer about locally approved control options.

Early detection helps reduce crop damage.
"""
    ),

    (
        r"\b(aphid|aphids)\b",

        """
### 🐛 Aphids in the garden

Aphids are small insects that feed on plant sap.

Signs include:

- Small insects on young leaves.
- Curled leaves.
- Sticky substances on plants.
- Weak plant growth.

Management:

1. Inspect the underside of leaves.
2. Remove heavily affected leaves where practical.
3. Encourage beneficial insects.
4. Keep the garden clean.
5. Ask an agricultural officer about suitable control methods.

Always follow product labels if an approved pesticide is recommended.
"""
    ),

    (
        r"\b(holes|hole)\b.*\b(cabbage|cabbages|leaves|leaf)\b|"
        r"\b(cabbage|cabbages)\b.*\b(holes|hole)\b",

        """
### 🥬 Holes in cabbage leaves

Possible causes include caterpillars, beetles and other insects.

What to do:

1. Check both sides of the leaves.
2. Look for caterpillars and insect eggs.
3. Inspect the plants regularly.
4. Remove visible pests where practical.
5. Seek local advice if the damage is serious.

Correct identification is important before choosing a treatment.
"""
    ),

    (
        r"\b(fungal disease|fungal diseases|fungus|fungi)\b",

        """
### 🌿 Identifying fungal diseases in crops

Possible signs include:

1. Spots on leaves.
2. White or powdery growth.
3. Mould-like growth.
4. Leaf yellowing.
5. Wilting or rotting.

Prevention:

- Avoid unnecessary overhead watering.
- Allow enough space between plants.
- Remove infected plant material safely.
- Keep tools and planting areas clean.
- Use healthy seeds and seedlings.

Different diseases have different symptoms. Ask an agricultural officer to confirm the disease.
"""
    ),

    (
        r"\b(disease|diseases)\b.*\b(tomato|tomatoes)\b|"
        r"\b(tomato|tomatoes)\b.*\b(disease|diseases)\b",

        """
### 🍅 Tomato plant diseases

Tomatoes can be affected by different diseases.

Possible warning signs include:

- Dark spots on leaves.
- Yellow leaves.
- Wilting.
- Rotting fruit.
- Unusual growth.

Prevention:

1. Use healthy seedlings.
2. Avoid overwatering.
3. Keep enough space between plants.
4. Remove diseased plant material.
5. Inspect plants regularly.

These symptoms can have several causes. Do not assume every yellow or spotted leaf is a disease.
"""
    ),

    (
        r"\b(maize|corn)\b.*\b(leaves|leaf)\b.*\b(dry|drying|brown)\b|"
        r"\b(dry|drying|brown)\b.*\b(maize|corn)\b",

        """
### 🌽 Drying maize leaves

Possible causes include:

1. Lack of water.
2. High temperatures.
3. Nutrient deficiencies.
4. Root problems.
5. Insect damage.
6. Plant diseases.

Check the soil moisture and inspect the leaves and stems.

If many plants are affected, contact an agricultural extension officer for further assessment.
"""
    ),

    (
        r"\b(prevent|prevention)\b.*\b(crop|crops|plant|plants)\b.*\b(disease|diseases)\b|"
        r"\b(crop|crops|plant|plants)\b.*\b(prevent|prevention)\b.*\b(disease|diseases)\b",

        """
### 🌱 Preventing crop diseases

1. Use healthy seeds and seedlings.
2. Keep the garden clean.
3. Avoid overcrowding plants.
4. Use proper watering methods.
5. Remove diseased plant material.
6. Control weeds.
7. Inspect crops regularly.
8. Rotate crops where appropriate.

Early detection can help prevent diseases from spreading.
"""
    ),

    (
        r"\b(protect|protection|control)\b.*\b(vegetable|vegetables)\b.*\b(insect|insects|pest|pests)\b|"
        r"\b(insect|insects|pest|pests)\b.*\b(vegetable|vegetables)\b",

        """
### 🥬 Protecting vegetables from insects

1. Inspect plants regularly.
2. Check the underside of leaves.
3. Remove visible pests where practical.
4. Keep the garden free from weeds.
5. Use physical barriers where suitable.
6. Encourage beneficial insects.
7. Identify pests before selecting a control method.

Ask an agricultural officer about approved pest-control products.
"""
    ),


    # -------------------------------------------------
    # 3. CATTLE FARMING
    # -------------------------------------------------

    (
        r"\b(signs|symptoms)\b.*\b(sick|ill)\b.*\b(cow|cattle)\b|"
        r"\b(sick|ill)\b.*\b(cow|cattle)\b",

        """
### 🐄 Signs of a sick cow

Possible warning signs include:

1. Refusing to eat or drink.
2. Unusual weakness.
3. Diarrhoea.
4. Coughing or difficulty breathing.
5. Unusual discharge.
6. Swelling.
7. Changes in behaviour.
8. Difficulty standing.

A veterinarian should examine an animal that appears seriously ill.
"""
    ),

    (
        r"\b(diarrhoea|diarrhea)\b.*\b(cattle|cow|cows)\b|"
        r"\b(cattle|cow|cows)\b.*\b(diarrhoea|diarrhea)\b",

        """
### 🐄 Diarrhoea in cattle

Possible causes include:

- Changes in feed.
- Poor-quality or contaminated water.
- Internal parasites.
- Bacterial or viral infections.
- Digestive problems.

What to do:

1. Contact a veterinarian for assessment.
2. Make clean drinking water available.
3. Observe the animal closely.
4. Avoid giving medicines without veterinary advice.
5. Seek urgent help if there is blood, severe weakness or dehydration.

Diarrhoea can become serious, especially in young calves.
"""
    ),

    (
        r"\b(drought|dry season)\b.*\b(cattle|cow|cows)\b|"
        r"\b(cattle|cow|cows)\b.*\b(drought|dry season)\b",

        """
### 🐄 Feeding cattle during drought

During drought, natural grazing may become limited.

Farmers can:

1. Provide clean drinking water.
2. Use good-quality hay or suitable stored forage.
3. Seek advice about balanced supplementary feed.
4. Monitor animal body condition.
5. Avoid sudden changes in feeding.
6. Keep poisonous plants away from livestock.
7. Consult an agricultural or livestock officer about available feed resources.

The correct feeding plan depends on the animal's age, condition and available feed.
"""
    ),

    (
        r"\b(prevent|prevention)\b.*\b(cattle|cow)\b.*\b(disease|diseases)\b|"
        r"\b(cattle|cow)\b.*\b(prevent|prevention)\b.*\b(disease|diseases)\b",

        """
### 🐄 Preventing cattle diseases

1. Follow a vaccination programme recommended by a veterinarian.
2. Provide clean drinking water.
3. Maintain good feeding.
4. Control ticks and parasites using approved methods.
5. Keep animal housing clean.
6. Check animals regularly.
7. Isolate sick animals when safe and seek veterinary advice.
8. Follow official livestock movement rules.

Prevention is generally easier than managing an outbreak.
"""
    ),

    (
        r"\b(cow|cattle)\b.*\b(refus|not eating|stop eating)\b|"
        r"\b(refus|not eating|stop eating)\b.*\b(cow|cattle)\b",

        """
### 🐄 Why a cow may refuse to eat

Possible causes include:

1. Illness or fever.
2. Poor-quality feed.
3. Digestive problems.
4. Dental or mouth problems.
5. Stress.
6. Pain.

Make clean water available and observe the animal.

Contact a veterinarian promptly, especially if the cow is weak, bloated or has stopped drinking. Do not try to diagnose it from this symptom alone.
"""
    ),

    (
        r"\b(common|most common)\b.*\b(cattle|cow)\b.*\b(disease|diseases)\b|"
        r"\b(cattle|cow)\b.*\b(disease|diseases)\b.*\b(namibia)\b",

        """
### 🐄 Cattle diseases in Namibia

Cattle can be affected by several types of diseases, including:

- Tick-borne diseases.
- Lumpy skin disease.
- Foot-and-mouth disease.
- Brucellosis.
- Respiratory infections.
- Internal and external parasites.

The diseases present and their risk vary by region and time.

For current disease information, vaccination requirements and outbreak warnings, contact your local State Veterinary Office or the Directorate of Veterinary Services in Namibia.

Do not move sick animals without veterinary advice.
"""
    ),

    (
        r"\b(improve|increase)\b.*\b(cattle)\b.*\b(growth|production|weight)\b|"
        r"\b(cattle)\b.*\b(growth|weight gain)\b",

        """
### 🐄 Improving cattle growth

1. Provide suitable and balanced feed.
2. Ensure constant access to clean water.
3. Maintain healthy grazing areas.
4. Follow veterinary vaccination recommendations.
5. Control parasites with professional guidance.
6. Provide suitable shelter.
7. Monitor animal health and body condition.

Good nutrition and health management support better growth.
"""
    ),

    (
        r"\b(why|importance|important)\b.*\b(vaccination|vaccines)\b.*\b(cattle|cow)\b|"
        r"\b(cattle|cow)\b.*\b(vaccination|vaccines)\b",

        """
### 💉 Why vaccination is important for cattle

Vaccination helps protect cattle against certain infectious diseases.

Benefits include:

1. Reducing the risk of specific diseases.
2. Reducing illness and deaths.
3. Supporting herd health.
4. Helping prevent disease outbreaks.

The correct vaccines and schedule depend on the area and disease risks. Follow advice from a veterinarian or State Veterinary Office.
"""
    ),


    # -------------------------------------------------
    # 4. GOAT AND SHEEP FARMING
    # -------------------------------------------------

    (
        r"\b(diarrhoea|diarrhea)\b.*\b(goat|goats)\b|"
        r"\b(goat|goats)\b.*\b(diarrhoea|diarrhea)\b",

        """
### 🐐 Diarrhoea in goats

Possible causes include:

- Sudden changes in feed.
- Internal parasites.
- Contaminated water.
- Infections.
- Digestive problems.

What to do:

1. Make clean water available.
2. Observe the goat carefully.
3. Contact a veterinarian.
4. Do not give medicines without professional advice.

Young goats can become seriously ill quickly. Seek urgent veterinary assistance if the goat is weak or dehydrated.
"""
    ),

    (
        r"\b(goat|goats)\b.*\b(lose weight|losing weight|thin|thinness)\b|"
        r"\b(losing weight|lose weight|thin)\b.*\b(goat|goats)\b",

        """
### 🐐 Why goats may lose weight

Possible causes include:

1. Poor nutrition.
2. Internal parasites.
3. Dental problems.
4. Chronic illness.
5. Competition for feed.
6. Poor-quality grazing.

Check the animal's feed and water supply.

A veterinarian should examine goats that continue losing weight or show other signs of illness.
"""
    ),

    (
        r"\b(what do|what should|feed)\b.*\b(goat|goats)\b",

        """
### 🐐 What do goats eat?

Goats are browsers and can eat a variety of suitable plants.

Their diet may include:

- Grass.
- Leaves and shrubs.
- Suitable hay.
- Appropriate supplementary feed.
- Clean drinking water.

Avoid poisonous plants and mouldy feed.

The feeding plan should match the goat's age, condition and production needs.
"""
    ),

    (
        r"\b(prevent|prevention)\b.*\b(sheep)\b.*\b(disease|diseases)\b|"
        r"\b(sheep)\b.*\b(prevent|prevention)\b.*\b(disease|diseases)\b",

        """
### 🐑 Preventing diseases in sheep

1. Follow a veterinary vaccination programme.
2. Provide clean water.
3. Give suitable feed.
4. Keep housing and resting areas clean.
5. Monitor for parasites.
6. Inspect sheep regularly.
7. Seek veterinary help when animals become sick.
8. Separate sick animals when safe.

Good management helps protect the flock.
"""
    ),

    (
        r"\b(internal parasites|worms|worm infestation)\b.*\b(goat|goats)\b|"
        r"\b(goat|goats)\b.*\b(internal parasites|worms|worm infestation)\b",

        """
### 🐐 Signs of internal parasites in goats

Possible signs include:

1. Weight loss.
2. Poor growth.
3. Diarrhoea.
4. Weakness.
5. Poor coat condition.
6. Pale lower eyelids in some parasite infections.

A veterinarian can confirm the problem through examination and suitable testing.

Avoid repeated or unnecessary deworming without professional guidance.
"""
    ),

    (
        r"\b(newborn|young)\b.*\b(lamb|lambs)\b|"
        r"\b(lamb|lambs)\b.*\b(newborn|care)\b",

        """
### 🐑 Caring for newborn lambs

1. Make sure the lamb can breathe normally.
2. Keep the lamb warm and dry.
3. Ensure it receives its mother's first milk, called colostrum, as soon as possible.
4. Check that the mother accepts and feeds the lamb.
5. Keep the lamb in a clean, safe area.
6. Monitor its activity and feeding.

Contact a veterinarian if the lamb cannot suckle, is weak or appears ill.
"""
    ),

    (
        r"\b(sheep)\b.*\b(cough|coughing)\b|"
        r"\b(cough|coughing)\b.*\b(sheep)\b",

        """
### 🐑 Why sheep may cough

Possible causes include:

- Dusty conditions.
- Respiratory infections.
- Lung parasites.
- Irritation from poor ventilation.

Keep the resting area clean and well ventilated.

If coughing continues or sheep have difficulty breathing, contact a veterinarian. Do not give medicines without professional advice.
"""
    ),

    (
        r"\b(improve|increase)\b.*\b(goat|goats)\b.*\b(production|growth)\b|"
        r"\b(goat|goats)\b.*\b(production|growth)\b",

        """
### 🐐 Improving goat production

1. Provide good-quality feed.
2. Ensure clean water is always available.
3. Choose healthy breeding animals.
4. Maintain clean housing.
5. Follow veterinary health recommendations.
6. Monitor newborn kids.
7. Protect goats from predators and extreme weather.

Good nutrition and proper management support healthy production.
"""
    ),


    # -------------------------------------------------
    # 5. POULTRY FARMING
    # -------------------------------------------------

    (
        r"\b(chicken|chickens|hen|hens)\b.*\b(not laying|laying eggs|eggs)\b|"
        r"\b(not laying eggs|egg laying)\b",

        """
### 🐔 Why chickens may stop laying eggs

Possible causes include:

1. Poor nutrition.
2. Lack of clean water.
3. Stress.
4. Disease.
5. Poor lighting conditions.
6. Age of the birds.
7. Changes in the environment.

Provide balanced poultry feed and clean water.

If birds also show signs of illness, contact a veterinarian.
"""
    ),

    (
        r"\b(newcastle)\b",

        """
### 🐔 Newcastle disease in chickens

Newcastle disease is a serious contagious viral disease of poultry.

Possible signs include:

- Difficulty breathing.
- Coughing or sneezing.
- Diarrhoea.
- Nervous system problems.
- Reduced egg production.
- Sudden deaths.

Prevention:

1. Follow a vaccination programme recommended by a veterinarian.
2. Keep poultry housing clean.
3. Limit contact with unfamiliar birds.
4. Control visitors and equipment movement.
5. Report suspected outbreaks to veterinary authorities.

If Newcastle disease is suspected, contact a veterinarian immediately. Do not move or sell affected birds.
"""
    ),

    (
        r"\b(prevent|prevention)\b.*\b(poultry|chicken|chickens)\b.*\b(disease|diseases)\b|"
        r"\b(poultry|chicken|chickens)\b.*\b(prevent|prevention)\b.*\b(disease|diseases)\b",

        """
### 🐔 Preventing poultry diseases

1. Keep chicken houses clean.
2. Provide clean drinking water.
3. Give balanced feed.
4. Follow recommended vaccination programmes.
5. Separate sick birds.
6. Avoid overcrowding.
7. Limit contact with wild birds.
8. Clean equipment regularly.

Good hygiene and biosecurity help protect poultry.
"""
    ),

    (
        r"\b(broiler|broilers)\b.*\b(feed|feeding|food)\b|"
        r"\b(feed|feeding)\b.*\b(broiler|broilers)\b",

        """
### 🐔 Feeding broiler chickens

Broilers need balanced feed for healthy growth.

Generally, feeding includes:

1. Starter feed for young chicks.
2. Grower feed as they develop.
3. Finisher feed as they approach market weight.

Provide clean water at all times.

Follow the feed manufacturer's instructions and seek local poultry advice about suitable feeding programmes.
"""
    ),

    (
        r"\b(chick|chicks)\b.*\b(dying|die|deaths)\b|"
        r"\b(dying|die)\b.*\b(chick|chicks)\b",

        """
### 🐔 Why chicks may be dying

Possible causes include:

1. Incorrect temperature.
2. Lack of clean water.
3. Poor feeding.
4. Infections.
5. Poor ventilation.
6. Overcrowding.
7. Contaminated housing.

What to do:

- Check the brooder temperature.
- Make sure water and feed are available.
- Keep the housing clean and dry.
- Contact a veterinarian immediately if chicks continue dying.

Several sudden deaths require urgent veterinary investigation.
"""
    ),

    (
        r"\b(clean|cleaning)\b.*\b(chicken house|poultry house|poultry housing)\b|"
        r"\b(chicken house|poultry house)\b.*\b(clean)\b",

        """
### 🐔 Cleaning a chicken house

Clean poultry housing regularly.

1. Remove manure and wet litter.
2. Wash suitable surfaces.
3. Clean drinkers and feeders.
4. Use an appropriate poultry-house disinfectant according to its label.
5. Allow the area to dry before adding fresh litter.
6. Maintain good ventilation.

How often cleaning is needed depends on the number and age of birds and the housing conditions.
"""
    ),

    (
        r"\b(diarrhoea|diarrhea)\b.*\b(chicken|chickens|poultry)\b|"
        r"\b(chicken|chickens|poultry)\b.*\b(diarrhoea|diarrhea)\b",

        """
### 🐔 Diarrhoea in chickens

Possible causes include:

- Contaminated water.
- Feed problems.
- Parasites.
- Bacterial or viral infections.
- Other digestive conditions.

Make clean water available and observe the birds.

Contact a veterinarian if several birds are affected, blood is present or birds become weak.
"""
    ),

    (
        r"\b(improve|increase)\b.*\b(egg|eggs)\b.*\b(production|laying)\b|"
        r"\b(egg|eggs)\b.*\b(production)\b",

        """
### 🥚 Improving egg production

1. Provide balanced layer feed.
2. Ensure clean water is always available.
3. Maintain clean nesting areas.
4. Provide suitable lighting.
5. Reduce unnecessary stress.
6. Maintain good ventilation.
7. Follow recommended vaccination programmes.
8. Monitor the health of the birds.

Healthy hens and proper management support good egg production.
"""
    ),


    # -------------------------------------------------
    # 6. SOIL, IRRIGATION AND GENERAL FARMING
    # -------------------------------------------------

    (
        r"\b(improve|increase)\b.*\b(soil fertility|fertility of soil)\b|"
        r"\b(soil fertility|fertility of soil)\b",

        """
### 🌱 Improving soil fertility

1. Add mature compost.
2. Use suitable well-rotted animal manure.
3. Rotate crops where appropriate.
4. Protect the soil from erosion.
5. Avoid unnecessary soil disturbance.
6. Test the soil to understand its nutrient needs.
7. Apply suitable fertiliser based on recommendations.

Healthy soil supports better crop growth.
"""
    ),

    (
        r"\b(difference)\b.*\b(organic|chemical)\b.*\b(fertiliser|fertilizer)\b|"
        r"\b(organic|chemical)\b.*\b(fertiliser|fertilizer)\b",

        """
### 🌱 Organic and chemical fertilisers

**Organic fertilisers**

- Come from materials such as compost and animal manure.
- Add organic matter to soil.
- Release nutrients at different rates.

**Chemical or mineral fertilisers**

- Contain specific plant nutrients.
- Often provide nutrients more quickly.
- Must be applied at the correct rate.

Both can support plant growth when used correctly. Soil testing helps farmers choose suitable fertilisers.
"""
    ),

    (
        r"\b(save|saving|conserve|conservation)\b.*\b(water)\b|"
        r"\b(water)\b.*\b(save|saving|conserve|conservation)\b",

        """
### 💧 Saving water on farms

1. Use drip irrigation where suitable.
2. Water near plant roots.
3. Check soil moisture before watering.
4. Water during cooler parts of the day.
5. Repair leaking pipes.
6. Use mulch to reduce evaporation.
7. Collect rainwater where permitted.
8. Avoid unnecessary watering.

Water conservation is especially important in dry areas of Namibia.
"""
    ),

    (
        r"\b(what is|explain|meaning)\b.*\b(drip irrigation)\b|"
        r"\b(drip irrigation)\b",

        """
### 💧 What is drip irrigation?

Drip irrigation is a watering method that delivers water slowly near plant roots through pipes and small outlets.

Advantages:

1. Reduces water waste.
2. Delivers water close to roots.
3. Can reduce weed growth between rows.
4. Helps maintain soil moisture.
5. Can be useful in dry areas.

The system needs proper installation and maintenance to prevent blockages.
"""
    ),

    (
        r"\b(drought)\b.*\b(crop|crops|farming|production)\b|"
        r"\b(crop|crops)\b.*\b(drought)\b",

        """
### ☀️ Effects of drought on crop production

Drought can cause:

1. Poor seed germination.
2. Slow plant growth.
3. Wilting.
4. Reduced harvests.
5. Poor fruit and grain development.
6. Increased crop losses.

Farmers can reduce drought impacts by:

- Choosing suitable crop varieties.
- Conserving soil moisture.
- Using water efficiently.
- Applying mulch.
- Following local agricultural advice.
"""
    ),

    (
        r"\b(compost)\b.*\b(make|prepare|how)\b|"
        r"\b(make|prepare|preparation)\b.*\b(compost)\b",

        """
### 🌱 Preparing compost

Compost can be made from suitable organic materials.

1. Collect dry leaves and plant material.
2. Add suitable green plant material.
3. Add small amounts of soil or mature compost.
4. Keep the mixture slightly moist.
5. Turn it regularly to allow air inside.
6. Allow the material to break down.

Avoid adding plastics, chemicals, diseased plants or animal waste that is unsuitable for composting.

Finished compost should be dark and crumbly.
"""
    ),

    (
        r"\b(dry areas|dry region|arid|semi.arid)\b.*\b(farming|crop|crops)\b|"
        r"\b(farming|crop|crops)\b.*\b(dry areas|dry region|arid|semi.arid)\b",

        """
### ☀️ Farming in dry areas

Farmers in dry areas can consider:

1. Drought-tolerant crop varieties.
2. Suitable crops such as pearl millet and sorghum.
3. Drip irrigation where water is available.
4. Mulching to conserve moisture.
5. Rainwater harvesting where permitted.
6. Soil conservation.
7. Careful livestock management.

The best choice depends on local rainfall, soil, water availability and market conditions.
"""
    ),

    (
        r"\b(reduce|prevent)\b.*\b(post.harvest|after harvest)\b.*\b(loss|losses)\b|"
        r"\b(post.harvest|after harvest)\b.*\b(loss|losses)\b",

        """
### 🌾 Reducing post-harvest losses

1. Harvest crops at the correct stage.
2. Handle produce carefully.
3. Remove damaged produce.
4. Use clean storage containers.
5. Keep stored crops in suitable conditions.
6. Protect produce from insects and rodents.
7. Transport produce carefully.
8. Sell or process produce before it spoils.

Good storage and handling reduce waste and protect farmers' income.
"""
    )
]


# =====================================================
# QUESTION RECOGNITION
# =====================================================

def split_questions(message):

    """
    Separates multiple questions in one message.
    Questions can be separated by question marks or new lines.
    """

    parts = re.split(r"\?+|\n+", message)

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def get_answer(question):

    q = question.lower().strip()

    # Greeting
    if re.fullmatch(
        r"(hi|hello|hey|good morning|good afternoon|good evening)[!. ]*",
        q
    ):
        return (
            "Hello! 🌱 Welcome to FarmAssist. "
            "I can help with crop farming, plant diseases, "
            "livestock, poultry, soil and irrigation. "
            "What would you like to know?"
        )

    # Match farming knowledge
    for pattern, answer in RULES:

        if re.search(pattern, q, re.IGNORECASE):
            return answer

    # General fallback
    return """
### 🌱 FarmAssist

I do not have enough information to answer that question yet.

I can currently help with:

- Tomato, maize, beans, cabbage and onion production.
- Plant diseases and crop pests.
- Cattle health and management.
- Goat and sheep farming.
- Poultry diseases and management.
- Soil fertility and fertilisers.
- Irrigation and water conservation.
- Drought and general farming practices.

Please try asking a more specific farming question.
"""


def get_multiple_answers(message):

    questions = split_questions(message)

    results = []

    for number, question in enumerate(questions, start=1):

        answer = get_answer(question)

        results.append(
            f"### Question {number}\n"
            f"**{question}**\n\n"
            f"{answer}"
        )

    return "\n\n---\n\n".join(results)


# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to FarmAssist! 🌱\n\n"
                "I can answer questions about crop farming, "
                "animal health, livestock, poultry, soil and irrigation.\n\n"
                "Type your farming question below to get started."
            )
        }
    ]


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🌱 FarmAssist")

    st.write("Agricultural Advisory Chatbot")

    st.divider()

    st.subheader("Farming topics")

    st.markdown("""
    🌱 Crop production

    🐛 Plant diseases and pests

    🐄 Cattle farming

    🐐 Goat and sheep farming

    🐔 Poultry farming

    💧 Soil and irrigation
    """)

    st.divider()

    st.subheader("Try a question")

    suggestions = [
        "How do I grow tomatoes?",
        "What causes yellow leaves in maize?",
        "Why is my cow not eating?",
        "What causes diarrhoea in goats?",
        "How can I prevent Newcastle disease in chickens?",
        "How can farmers save water?"
    ]

    for index, suggestion in enumerate(suggestions):

        if st.button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True
        ):
            st.session_state.pending_question = suggestion

    st.divider()

    if st.button("🗑️ Clear conversation", use_container_width=True):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! 🌱 Welcome to FarmAssist. What farming question can I help you with?"
            }
        ]

        st.rerun()


# =====================================================
# DISPLAY CHAT MESSAGES
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# =====================================================
# CHAT INPUT
# =====================================================

typed_question = st.chat_input(
    "Ask FarmAssist about crops, animals or farming..."
)

pending_question = st.session_state.pop(
    "pending_question",
    None
)

question = typed_question if typed_question else pending_question


# =====================================================
# PROCESS FARMING QUESTIONS
# =====================================================

if question:

    # Display farmer's question
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    # Generate answer
    answer = get_multiple_answers(question)

    # Save chatbot answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "🌱 FarmAssist | Agricultural Advisory Chatbot"
)

st.caption(
    "This prototype provides general farming information. "
    "For serious crop or animal health problems, consult a "
    "qualified agricultural or veterinary professional."
)
