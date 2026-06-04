import streamlit as st
import geopandas as gpd
import math
import tempfile
import zipfile
import os
from pathlib import Path
from PIL import Image
from geopy.geocoders import Nominatim


APP_NAME = "Meridiana"
APP_VERSION = "v1.0.0"

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "logo.png"

if LOGO_PATH.exists():
    logo_icon = Image.open(LOGO_PATH)
else:
    logo_icon = "🌍"

st.set_page_config(
    page_title=APP_NAME,
    page_icon=logo_icon,
    layout="centered"
)


LANG = {
    "English": {
        "subtitle": "Coordinate Reference System Recommendation Tool",
        "description": "Automatic CRS recommendation for places, coordinates and georeferenced vector files.",
        "author": "Elaborated by Alexandre Castro, PhD.",
        "active_language": "Active language",
        "input_method": "Choose the input method:",
        "place": "Place name",
        "coords": "Latitude and longitude",
        "vector": "Georeferenced vector file",
        "place_label": "Enter the place name:",
        "place_default": "João Pessoa, Brazil",
        "search": "Find CRS",
        "clear": "Clear",
        "country": "Country:",
        "study_country": "Study area country:",
        "brazil": "Brazil",
        "outside_brazil": "Outside Brazil",
        "auto_detect": "Auto-detect country from file centroid",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "utm": "UTM Zone",
        "considered_country": "Considered country",
        "recommended": "Recommended CRS",
        "upload": "Upload a GPKG, GeoJSON or ZIP containing SHP:",
        "original_crs": "Original file CRS",
        "not_found": "Place not found.",
        "no_shp": "No .shp file found inside the ZIP.",
        "empty_file": "The file is empty.",
        "missing_crs": "The file has no defined CRS. It is not possible to safely identify its location.",
        "invalid_coords": "Invalid coordinates. Latitude must be between -90 and 90, and longitude between -180 and 180.",
        "technical_summary": "Technical summary",
        "datum": "Datum",
        "projection": "Projection",
        "epsg": "EPSG code",
        "copy_epsg": "Copy EPSG code",
        "copied": "Copied!",
        "justification": "Justification",
        "justification_brazil": "This CRS is recommended because it uses SIRGAS 2000 with the corresponding UTM zone, which is suitable for measurements of area, distance, perimeter and urban spatial analysis in Brazil.",
        "justification_other": "This CRS is recommended because it uses WGS 84 with the corresponding UTM zone, which is suitable for local measurements of area, distance and perimeter outside Brazil.",
        "multi_zone_warning": "Warning: the vector layer appears to cross more than one UTM zone. The recommendation is based on the layer centroid and may not be ideal for very large areas.",
        "detected_country": "Detected country",
        "country_detection_failed": "Country auto-detection failed. Please select the study area country manually.",
        "method_title": "Method",
        "method_text": "Brazil uses SIRGAS 2000 / UTM in the corresponding UTM zone. Areas outside Brazil use WGS 84 / UTM in the corresponding UTM zone. The UTM zone is calculated from longitude. For vector files, the centroid of the unified geometry is used.",
    },
    "Português": {
        "subtitle": "Ferramenta de Recomendação de Sistemas de Referência de Coordenadas",
        "description": "Recomendação automática de SRC para locais, coordenadas e arquivos vetoriais georreferenciados.",
        "author": "Elaborado por Alexandre Castro, PhD.",
        "active_language": "Idioma ativo",
        "input_method": "Escolha a forma de entrada:",
        "place": "Nome do local",
        "coords": "Latitude e longitude",
        "vector": "Arquivo vetorial georreferenciado",
        "place_label": "Digite o nome do local:",
        "place_default": "João Pessoa, Brasil",
        "search": "Identificar SRC",
        "clear": "Limpar",
        "country": "País:",
        "study_country": "País da área de estudo:",
        "brazil": "Brasil",
        "outside_brazil": "Fora do Brasil",
        "auto_detect": "Detectar país automaticamente pelo centroide do arquivo",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "utm": "Zona UTM",
        "considered_country": "País considerado",
        "recommended": "SRC recomendado",
        "upload": "Envie um arquivo GPKG, GeoJSON ou ZIP contendo SHP:",
        "original_crs": "SRC original do arquivo",
        "not_found": "Local não encontrado.",
        "no_shp": "Nenhum arquivo .shp encontrado no ZIP.",
        "empty_file": "O arquivo está vazio.",
        "missing_crs": "O arquivo não possui SRC definido. Não é possível identificar sua localização com segurança.",
        "invalid_coords": "Coordenadas inválidas. A latitude deve estar entre -90 e 90, e a longitude entre -180 e 180.",
        "technical_summary": "Resumo técnico",
        "datum": "Datum",
        "projection": "Projeção",
        "epsg": "Código EPSG",
        "copy_epsg": "Copiar código EPSG",
        "copied": "Copiado!",
        "justification": "Justificativa",
        "justification_brazil": "Este SRC é recomendado porque utiliza SIRGAS 2000 com a zona UTM correspondente, sendo adequado para medidas de área, distância, perímetro e análises espaciais urbanas no Brasil.",
        "justification_other": "Este SRC é recomendado porque utiliza WGS 84 com a zona UTM correspondente, sendo adequado para medidas locais de área, distância e perímetro fora do Brasil.",
        "multi_zone_warning": "Atenção: a camada vetorial parece cruzar mais de uma zona UTM. A recomendação foi baseada no centroide da camada e pode não ser ideal para áreas muito extensas.",
        "detected_country": "País detectado",
        "country_detection_failed": "Não foi possível detectar o país automaticamente. Selecione manualmente o país da área de estudo.",
        "method_title": "Método",
        "method_text": "No Brasil, o aplicativo recomenda SIRGAS 2000 / UTM na zona UTM correspondente. Fora do Brasil, recomenda WGS 84 / UTM na zona UTM correspondente. A zona UTM é calculada a partir da longitude. Para arquivos vetoriais, utiliza-se o centroide da geometria unificada.",
    },
    "Español": {
        "subtitle": "Herramienta de Recomendación de Sistemas de Referencia de Coordenadas",
        "description": "Recomendación automática de SRC para lugares, coordenadas y archivos vectoriales georreferenciados.",
        "author": "Elaborado por Alexandre Castro, PhD.",
        "active_language": "Idioma activo",
        "input_method": "Seleccione el método de entrada:",
        "place": "Nombre del lugar",
        "coords": "Latitud y longitud",
        "vector": "Archivo vectorial georreferenciado",
        "place_label": "Ingrese el nombre del lugar:",
        "place_default": "João Pessoa, Brasil",
        "search": "Identificar SRC",
        "clear": "Limpar",
        "country": "País:",
        "study_country": "País del área de estudio:",
        "brazil": "Brasil",
        "outside_brazil": "Fuera de Brasil",
        "auto_detect": "Detectar país automáticamente por el centroide del archivo",
        "latitude": "Latitud",
        "longitude": "Longitud",
        "utm": "Zona UTM",
        "considered_country": "País considerado",
        "recommended": "SRC recomendado",
        "upload": "Suba un archivo GPKG, GeoJSON o ZIP que contenga SHP:",
        "original_crs": "SRC original del archivo",
        "not_found": "Lugar no encontrado.",
        "no_shp": "No se encontró ningún archivo .shp en el ZIP.",
        "empty_file": "El archivo está vacío.",
        "missing_crs": "El archivo no tiene un SRC definido. No es posible identificar su ubicación con seguridad.",
        "invalid_coords": "Coordenadas inválidas. La latitud debe estar entre -90 y 90, y la longitud entre -180 y 180.",
        "technical_summary": "Resumen técnico",
        "datum": "Datum",
        "projection": "Proyección",
        "epsg": "Código EPSG",
        "copy_epsg": "Copiar código EPSG",
        "copied": "Copiado!",
        "justification": "Justificación",
        "justification_brazil": "Este SRC se recomienda porque utiliza SIRGAS 2000 con la zona UTM correspondiente, adecuado para mediciones de área, distancia, perímetro y análisis espaciales urbanos en Brasil.",
        "justification_other": "Este SRC se recomienda porque utiliza WGS 84 con la zona UTM correspondiente, adecuado para mediciones locales de área, distancia y perímetro fuera de Brasil.",
        "multi_zone_warning": "Advertencia: la capa vectorial parece cruzar más de una zona UTM. La recomendación se basa en el centroide de la capa y puede no ser ideal para áreas muy extensas.",
        "detected_country": "País detectado",
        "country_detection_failed": "No fue posible detectar el país automáticamente. Seleccione manualmente el país del área de estudio.",
        "method_title": "Método",
        "method_text": "En Brasil, la aplicación recomienda SIRGAS 2000 / UTM en la zona UTM correspondiente. Fuera de Brasil, recomienda WGS 84 / UTM en la zona UTM correspondiente. La zona UTM se calcula a partir de la longitud. Para archivos vectoriales, se utiliza el centroide de la geometría unificada.",
    },
    "Français": {
        "subtitle": "Outil de Recommandation des Systèmes de Référence de Coordonnées",
        "description": "Recommandation automatique de SCR pour les lieux, les coordonnées et les fichiers vectoriels géoréférencés.",
        "author": "Élaboré par Alexandre Castro, PhD.",
        "active_language": "Langue active",
        "input_method": "Choisissez la méthode d'entrée :",
        "place": "Nom du lieu",
        "coords": "Latitude et longitude",
        "vector": "Fichier vectoriel géoréférencé",
        "place_label": "Saisissez le nom du lieu :",
        "place_default": "João Pessoa, Brésil",
        "search": "Identifier le SCR",
        "clear": "Effacer",
        "country": "Pays :",
        "study_country": "Pays de la zone d'étude :",
        "brazil": "Brésil",
        "outside_brazil": "Hors du Brésil",
        "auto_detect": "Détecter automatiquement le pays à partir du centroïde du fichier",
        "latitude": "Latitude",
        "longitude": "Longitude",
        "utm": "Zone UTM",
        "considered_country": "Pays considéré",
        "recommended": "SCR recommandé",
        "upload": "Téléchargez un fichier GPKG, GeoJSON ou ZIP contenant un SHP :",
        "original_crs": "SCR original du fichier",
        "not_found": "Lieu introuvable.",
        "no_shp": "Aucun fichier .shp trouvé dans le ZIP.",
        "empty_file": "Le fichier est vide.",
        "missing_crs": "Le fichier n'a pas de SCR défini. Il n'est pas possible d'identifier son emplacement en toute sécurité.",
        "invalid_coords": "Coordonnées invalides. La latitude doit être comprise entre -90 et 90, et la longitude entre -180 et 180.",
        "technical_summary": "Résumé technique",
        "datum": "Datum",
        "projection": "Projection",
        "epsg": "Code EPSG",
        "copy_epsg": "Copier le code EPSG",
        "copied": "Copié !",
        "justification": "Justification",
        "justification_brazil": "Ce SCR est recommandé car il utilise SIRGAS 2000 avec la zone UTM correspondante, adapté aux mesures de surface, distance, périmètre et aux analyses spatiales urbaines au Brésil.",
        "justification_other": "Ce SCR est recommandé car il utilise WGS 84 avec la zone UTM correspondante, adapté aux mesures locales de surface, distance et périmètre hors du Brésil.",
        "multi_zone_warning": "Attention : la couche vectorielle semble traverser plus d'une zone UTM. La recommandation est basée sur le centroïde de la couche et peut ne pas être idéale pour les très grandes zones.",
        "detected_country": "Pays détecté",
        "country_detection_failed": "La détection automatique du pays a échoué. Veuillez sélectionner manuellement le pays de la zone d'étude.",
        "method_title": "Méthode",
        "method_text": "Au Brésil, l'application recommande SIRGAS 2000 / UTM dans la zone UTM correspondante. Hors du Brésil, elle recommande WGS 84 / UTM dans la zone UTM correspondante. La zone UTM est calculée à partir de la longitude. Pour les fichiers vectoriels, le centroïde de la géométrie unifiée est utilisé.",
    },
}

LANGUAGE_OPTIONS = ["English", "Português", "Español", "Français"]


if "language" not in st.session_state:
    st.session_state.language = "English"


def render_language_selector():
    """Render a compact language selector using native language names."""
    cols = st.columns(len(LANGUAGE_OPTIONS))

    for col, language_name in zip(cols, LANGUAGE_OPTIONS):
        is_active = st.session_state.language == language_name
        label = f"✓ {language_name}" if is_active else language_name

        with col:
            if st.button(label, key=f"lang_{language_name}", use_container_width=True):
                st.session_state.language = language_name


def clear_app_state():
    """Clear user inputs and results while preserving the selected language."""
    current_language = st.session_state.language
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.language = current_language
    st.rerun()


def utm_zone(lon):
    return math.floor((lon + 180) / 6) + 1


def validate_coordinates(lat, lon):
    return -90 <= lat <= 90 and -180 <= lon <= 180


def is_brazil(country=""):
    country_lower = country.lower()
    return any(term in country_lower for term in ["brasil", "brazil", "brésil"])


def recommend_crs(lat, lon, country=""):
    zone = utm_zone(lon)
    south = lat < 0

    if is_brazil(country):
        epsg_num = 31960 + zone
        name = f"SIRGAS 2000 / UTM zone {zone}S"
        datum = "SIRGAS 2000"
        projection = f"UTM zone {zone}S"
        return name, f"EPSG:{epsg_num}", zone, datum, projection, True

    if south:
        epsg_num = 32700 + zone
        name = f"WGS 84 / UTM zone {zone}S"
        projection = f"UTM zone {zone}S"
    else:
        epsg_num = 32600 + zone
        name = f"WGS 84 / UTM zone {zone}N"
        projection = f"UTM zone {zone}N"

    return name, f"EPSG:{epsg_num}", zone, "WGS 84", projection, False


def normalize_country(country):
    if is_brazil(country):
        return "Brazil"
    return country


@st.cache_data(show_spinner=False)
def geocode_place(place):
    geolocator = Nominatim(user_agent="meridiana_app")
    location = geolocator.geocode(place, addressdetails=True)
    if location is None:
        return None

    return {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "address": location.raw.get("address", {}),
    }


@st.cache_data(show_spinner=False)
def reverse_geocode_country(lat, lon):
    geolocator = Nominatim(user_agent="meridiana_app")
    location = geolocator.reverse((lat, lon), addressdetails=True, language="en")
    if location is None:
        return None

    return location.raw.get("address", {}).get("country")


def read_vector_file(uploaded_file):
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if uploaded_file.name.lower().endswith(".zip"):
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                zip_ref.extractall(tmpdir)

            shp_files = []

            for root, dirs, files in os.walk(tmpdir):
                for file in files:
                    if file.lower().endswith(".shp"):
                        shp_files.append(os.path.join(root, file))

            if not shp_files:
                st.error(T["no_shp"])
                st.stop()

            gdf = gpd.read_file(shp_files[0])

        else:
            gdf = gpd.read_file(file_path)

    return gdf


def get_vector_centroid_and_zones(gdf):
    gdf_wgs84 = gdf.to_crs(epsg=4326)
    unified_geom = gdf_wgs84.geometry.union_all()
    centroid = unified_geom.centroid

    minx, miny, maxx, maxy = gdf_wgs84.total_bounds
    min_zone = utm_zone(minx)
    max_zone = utm_zone(maxx)
    crosses_multiple_zones = min_zone != max_zone

    return centroid.y, centroid.x, crosses_multiple_zones, min_zone, max_zone


def show_result(lat, lon, country, crosses_multiple_zones=False, zone_range=None):
    if not validate_coordinates(lat, lon):
        st.error(T["invalid_coords"])
        return

    country = normalize_country(country)
    name, epsg, zone, datum, projection, brazil_rule = recommend_crs(lat, lon, country)

    st.markdown(
        f"**{T['latitude']}:** {lat:.6f}<br>"
        f"**{T['longitude']}:** {lon:.6f}<br>"
        f"**{T['utm']}:** {zone}<br>"
        f"**{T['considered_country']}:** {country}",
        unsafe_allow_html=True,
    )

    st.success(f"{T['recommended']}: **{name} — {epsg}**")

    if crosses_multiple_zones:
        if zone_range:
            st.warning(f"{T['multi_zone_warning']} ({zone_range[0]}–{zone_range[1]})")
        else:
            st.warning(T["multi_zone_warning"])


render_language_selector()

language = st.session_state.language
T = LANG[language]

st.markdown(
    f"<p style='text-align:center; margin-top:-0.25rem;'><strong>🌐 {T['active_language']}: {language}</strong></p>",
    unsafe_allow_html=True,
)

col_logo, col_text = st.columns([1, 5])

with col_logo:
    if LOGO_PATH.exists():
        st.image(str(LOGO_PATH), width=90)
    else:
        st.markdown("# 🌍")

with col_text:
    st.title(APP_NAME)

    st.markdown(
        f"""
        <div style="line-height:1.0; color:gray;">
            <div style="font-size:0.90rem;">
                {T['subtitle']}
            </div>
            <div style="font-size:0.80rem;">
                {APP_VERSION}
            </div>
            <div style="font-size:0.82rem; margin-bottom:18px;">
                {T['author']}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with st.expander(T["method_title"], expanded=False):
    st.write(T["method_text"])

option = st.radio(
    T["input_method"],
    [
        T["place"],
        T["coords"],
        T["vector"],
    ],
)

if option == T["place"]:
    place = st.text_input(
        T["place_label"],
        T["place_default"],
    )

    col_search, col_clear = st.columns([4, 1])

    with col_search:
        search_clicked = st.button(T["search"], use_container_width=True, key="search_place")

    with col_clear:
        clear_clicked = st.button(T["clear"], use_container_width=True, key="clear_place")

    if clear_clicked:
        clear_app_state()

    if search_clicked:
        location = geocode_place(place)

        if location is None:
            st.error(T["not_found"])
        else:
            lat = location["latitude"]
            lon = location["longitude"]
            address = location["address"]
            country = address.get("country", "")

            show_result(lat, lon, country)

elif option == T["coords"]:
    lat = st.number_input(
        f"{T['latitude']}:",
        min_value=-90.0,
        max_value=90.0,
        value=-7.2342,
        format="%.6f",
    )

    lon = st.number_input(
        f"{T['longitude']}:",
        min_value=-180.0,
        max_value=180.0,
        value=-39.4093,
        format="%.6f",
    )

    country = st.selectbox(
        T["country"],
        [T["brazil"], T["outside_brazil"]],
    )

    col_search, col_clear = st.columns([4, 1])

    with col_search:
        search_clicked = st.button(T["search"], use_container_width=True, key="search_coords")

    with col_clear:
        clear_clicked = st.button(T["clear"], use_container_width=True, key="clear_coords")

    if clear_clicked:
        clear_app_state()

    if search_clicked:
        show_result(lat, lon, country)

elif option == T["vector"]:
    uploaded_file = st.file_uploader(
        T["upload"],
        type=["gpkg", "geojson", "json", "zip"],
    )

    auto_detect_country = st.checkbox(T["auto_detect"], value=True)

    country = None
    if not auto_detect_country:
        country = st.selectbox(
            T["study_country"],
            [T["brazil"], T["outside_brazil"]],
        )

    col_search, col_clear = st.columns([4, 1])

    with col_search:
        process_clicked = st.button(T["search"], use_container_width=True, key="search_vector")

    with col_clear:
        clear_clicked = st.button(T["clear"], use_container_width=True, key="clear_vector")

    if clear_clicked:
        clear_app_state()

    if uploaded_file is not None and process_clicked:
        gdf = read_vector_file(uploaded_file)

        if gdf.empty:
            st.error(T["empty_file"])
            st.stop()

        if gdf.crs is None:
            st.error(T["missing_crs"])
            st.stop()

        lat, lon, crosses_multiple_zones, min_zone, max_zone = get_vector_centroid_and_zones(gdf)

        if auto_detect_country:
            detected_country = reverse_geocode_country(lat, lon)
            if detected_country:
                country = detected_country
                st.write(f"**{T['detected_country']}:** {country}")
            else:
                st.warning(T["country_detection_failed"])
                country = st.selectbox(
                    T["study_country"],
                    [T["brazil"], T["outside_brazil"]],
                )

        st.write(f"**{T['original_crs']}:** {gdf.crs}")

        show_result(
            lat,
            lon,
            country,
            crosses_multiple_zones=crosses_multiple_zones,
            zone_range=(min_zone, max_zone),
        )
