"""
Datos geográficos estáticos de Chile para EduCompra Humm.
16 Regiones oficiales con sus respectivas comunas.
No depende de APIs externas ni servicios de terceros.
"""

REGIONES_CHILE = [
    {
        "nombre": "Arica y Parinacota",
        "numero": "XV",
        "comunas": ["Arica", "Camarones", "Putre", "General Lagos"]
    },
    {
        "nombre": "Tarapacá",
        "numero": "I",
        "comunas": ["Iquique", "Alto Hospicio", "Pozo Almonte", "Camiña", "Colchane", "Huara", "Pica"]
    },
    {
        "nombre": "Antofagasta",
        "numero": "II",
        "comunas": [
            "Antofagasta", "Mejillones", "Sierra Gorda", "Taltal",
            "Calama", "Ollagüe", "San Pedro de Atacama", "Tocopilla", "María Elena"
        ]
    },
    {
        "nombre": "Atacama",
        "numero": "III",
        "comunas": [
            "Copiapó", "Caldera", "Tierra Amarilla", "Chañaral", "Diego de Almagro",
            "Vallenar", "Alto del Carmen", "Freirina", "Huasco"
        ]
    },
    {
        "nombre": "Coquimbo",
        "numero": "IV",
        "comunas": [
            "La Serena", "Coquimbo", "Andacollo", "La Higuera", "Paiguano", "Vicuña",
            "Illapel", "Canela", "Los Vilos", "Salamanca",
            "Ovalle", "Combarbalá", "Monte Patria", "Punitaqui", "Río Hurtado"
        ]
    },
    {
        "nombre": "Valparaíso",
        "numero": "V",
        "comunas": [
            "Valparaíso", "Casablanca", "Concón", "Juan Fernández", "Puchuncaví", "Quintero", "Viña del Mar",
            "Isla de Pascua", "Los Andes", "Calle Larga", "Rinconada", "San Esteban",
            "La Ligua", "Cabildo", "Papudo", "Petorca", "Zapallar",
            "Quillota", "Calera", "Hijuelas", "La Cruz", "Nogales",
            "San Antonio", "Algarrobo", "Cartagena", "El Quisco", "El Tabo", "Santo Domingo",
            "San Felipe", "Catemu", "Llaillay", "Panquehue", "Putaendo", "Santa María",
            "Quilpué", "Limache", "Olmué", "Villa Alemana"
        ]
    },
    {
        "nombre": "Metropolitana de Santiago",
        "numero": "RM",
        "comunas": [
            "Santiago", "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central",
            "Huechurba", "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana",
            "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú",
            "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura",
            "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura",
            "Puente Alto", "Pirque", "San José de Maipo",
            "Colina", "Lampa", "Tiltil",
            "San Bernardo", "Buin", "Calera de Tango", "Paine",
            "Melipilla", "Alhué", "Curacaví", "María Pinto", "San Pedro",
            "Talagante", "El Monte", "Isla de Maipo", "Padre Hurtado", "Peñaflor"
        ]
    },
    {
        "nombre": "Libertador General Bernardo O'Higgins",
        "numero": "VI",
        "comunas": [
            "Rancagua", "Codegua", "Coinco", "Coltauco", "Doñihue", "Graneros", "Las Cabras",
            "Machalí", "Malloa", "Mostazal", "Olivar", "Peumo", "Pichidegua", "Quinta de Tilcoco",
            "Rengo", "Requínoa", "San Vicente",
            "Pichilemu", "La Estrella", "Litueche", "Marchihue", "Navidad", "Paredones",
            "San Fernando", "Chépica", "Chimbarongo", "Lolol", "Nancagua", "Palmilla", "Peralillo",
            "Placilla", "Pumanque", "Santa Cruz"
        ]
    },
    {
        "nombre": "Maule",
        "numero": "VII",
        "comunas": [
            "Talca", "Constitución", "Curepto", "Empedrado", "Maule", "Pelarco", "Pencahue", "Río Claro", "San Clemente", "San Rafael",
            "Cauquenes", "Chanco", "Pelluhue",
            "Curicó", "Hualañé", "Licantén", "Molina", "Rauco", "Romeral", "Sagrada Familia", "Teno", "Vichuquén",
            "Linares", "Colbún", "Longaví", "Parral", "Retiro", "San Javier", "Villa Alegre", "Yerbas Buenas"
        ]
    },
    {
        "nombre": "Ñuble",
        "numero": "XVI",
        "comunas": [
            "Chillán", "Bulnes", "Cobquecura", "Coelemu", "Coihueco", "Chillán Viejo", "El Carmen",
            "Ninhue", "Ñiquén", "Pemuco", "Pinto", "Portezuelo", "Quillón", "Quirihue", "Ránquil",
            "San Carlos", "San Fabián", "San Ignacio", "San Nicolás", "Treguaco", "Yungay"
        ]
    },
    {
        "nombre": "Biobío",
        "numero": "VIII",
        "comunas": [
            "Concepción", "Coronel", "Chiguayante", "Florida", "Hualqui", "Lota", "Penco", "San Pedro de la Paz", "Santa Juana", "Talcahuano", "Tomé", "Hualpén",
            "Lebu", "Arauco", "Cañete", "Contulmo", "Curanilahue", "Los Álamos", "Tirúa",
            "Los Ángeles", "Antuco", "Cabrero", "Laja", "Mulchén", "Nacimiento", "Negrete", "Quilaco", "Quilleco", "San Rosendo", "Santa Bárbara", "Tucapel", "Yumbel", "Alto Biobío"
        ]
    },
    {
        "nombre": "La Araucanía",
        "numero": "IX",
        "comunas": [
            "Temuco", "Carahue", "Cunco", "Curarrehue", "Freire", "Galvarino", "Gorbea", "Lautaro", "Loncoche", "Melipeuco", "Nueva Imperial", "Padre Las Casas", "Perquenco", "Pitrufquén", "Pucón", "Saavedra", "Teodoro Schmidt", "Toltén", "Vilcún", "Villarrica", "Cholchol",
            "Angol", "Collipulli", "Curacautín", "Ercilla", "Lonquimay", "Los Sauces", "Lumaco", "Purén", "Renaico", "Traiguén", "Victoria"
        ]
    },
    {
        "nombre": "Los Ríos",
        "numero": "XIV",
        "comunas": [
            "Valdivia", "Corral", "Lanco", "Los Lagos", "Máfil", "Mariquina", "Paillaco", "Panguipulli",
            "La Unión", "Futrono", "Lago Ranco", "Río Bueno"
        ]
    },
    {
        "nombre": "Los Lagos",
        "numero": "X",
        "comunas": [
            "Puerto Montt", "Calbuco", "Cochamó", "Fresia", "Frutillar", "Los Muermos", "Llanquihue", "Maullín", "Puerto Varas",
            "Castro", "Ancud", "Chonchi", "Curaco de Vélez", "Dalcahue", "Puqueldón", "Queilén", "Quellón", "Quemchi", "Quinchao",
            "Osorno", "Puerto Octay", "Purranque", "Puyehue", "Río Negro", "San Juan de la Costa", "San Pablo",
            "Chaitén", "Futaleufú", "Hualaihué", "Palena"
        ]
    },
    {
        "nombre": "Aysén del General Carlos Ibáñez del Campo",
        "numero": "XI",
        "comunas": [
            "Coyhaique", "Lago Verde",
            "Aysén", "Cisnes", "Guaitecas",
            "Cochrane", "O'Higgins", "Tortel",
            "Chile Chico", "Río Ibáñez"
        ]
    },
    {
        "nombre": "Magallanes y de la Antártica Chilena",
        "numero": "XII",
        "comunas": [
            "Punta Arenas", "Laguna Blanca", "Río Verde", "San Gregorio",
            "Cabo de Hornos", "Antártica",
            "Porvenir", "Primavera", "Timaukel",
            "Natales", "Torres del Paine"
        ]
    }
]

def obtener_regiones_comunas_dict():
    """Retorna un diccionario { 'Nombre Región': ['Comuna 1', 'Comuna 2', ...] }"""
    return {r["nombre"]: sorted(r["comunas"]) for r in REGIONES_CHILE}

def obtener_nombres_regiones():
    """Retorna lista ordenada de nombres de regiones."""
    return [r["nombre"] for r in REGIONES_CHILE]
