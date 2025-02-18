/* Archivo model.mod */
/* Modelo revisado de asignación de llamadas a parkings de ambulancias con localizaciones y costos adicionales */


/* Conjuntos */
set DISTRICTS; /* Conjunto de distritos */
set PARKINGS;  /* Conjunto de parkings de ambulancias */

/* Parámetros */
param calls{DISTRICTS} >= 0;    /* Número de llamadas de cada distrito */
param time{DISTRICTS, PARKINGS} >= 0; /* Tiempo que tarda una ambulancia en llegar a cada distrito desde un parking */
param fixedCost{PARKINGS} >= 0; /* Costo fijo de establecer un parking */
param M > 0;
param variableCost >= 0;

/* Variables de decisión */
var x{DISTRICTS, PARKINGS} >= 0, integer; /* Número de llamadas del distrito i atendidas por el parking j */
var y{PARKINGS} binary; /* 1 si se selecciona el parking j, 0 en caso contrario */
var w{DISTRICTS} binary; /* 1 si el distrito i tiene un alto volumen de llamadas, 0 en caso contrario */
var z{DISTRICTS, PARKINGS} binary; /* 1 si el distrito i es atendido por el parking j, 0 en caso contrario */

/* Función objetivo: Minimizar el costo total, incluyendo el costo de establecimiento y operacional */
minimize TotalCost: sum{i in DISTRICTS, j in PARKINGS} variableCost * time[i,j] * x[i,j] + sum{j in PARKINGS} fixedCost[j] * y[j];


/* Restricciones */

/* Asegura que todas las llamadas sean atendidas */
s.t. AttendAllCalls{i in DISTRICTS}: sum{j in PARKINGS} x[i,j] = calls[i];

/* Limita la asignación a la capacidad del parking */
s.t. ParkingCapacity{j in PARKINGS}: sum{i in DISTRICTS} x[i,j] <= M * y[j];

/* Asegura que el tiempo de viaje para cada asignación no excede los 35 minutos */
s.t. TravelTime{i in DISTRICTS, j in PARKINGS}: time[i,j] * x[i,j] <= 35 * x[i,j];

/* Garantiza que cada parking seleccionado atienda al menos un distrito */
s.t. ParkingUsage{j in PARKINGS}: sum{i in DISTRICTS} z[i,j] >= y[j];

/* Identifica distritos con alto volumen de llamadas */
s.t. HighVolumeIndicator1{i in DISTRICTS}: w[i] <= (calls[i]/7500);
s.t. HighVolumeIndicator2{i in DISTRICTS}: w[i] >= (calls[i] - 7500) / M;


/* Asegura que los distritos de alto volumen sean atendidos por al menos dos parkings */
s.t. HighVolumeCalls{i in DISTRICTS}: sum{j in PARKINGS} z[i,j] >= 2 * w[i];

/* Asegura que un parking atienda al menos el 10% de las llamadas de un distrito si está asignado a ese distrito */
s.t. MinimumCoverage{i in DISTRICTS, j in PARKINGS}: x[i,j] >= 0.1 * calls[i] * z[i,j];

/* Asegura que z[i,j] se establece correctamente */
s.t. SetZVariable{i in DISTRICTS, j in PARKINGS}: z[i,j] <= (M * x[i,j]) / (0.1 * calls[i]);


end;
