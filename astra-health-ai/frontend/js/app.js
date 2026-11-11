
async function simulateData() {

    try {

        // 1. Consultamos al backend mediante una solicitud HTTP GET
        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/health"
        );

        // 2. Comprobamos si el servidor respondió correctamente
        if (!response.ok) {
            throw new Error("No fue posible obtener los indicadores.");
        }

        // 3. Convertimos la respuesta JSON en un objeto JavaScript
        const data = await response.json();

        // 4. Extraemos los indicadores enviados por FastAPI
        const heart = data.heart_rate;
        const oxygen = data.oxygen_saturation;
        const sleep = data.sleep_hours;

        // 5. La actividad todavía se simula en el frontend
        const activity = data.activity;
        
        // 6. Actualizamos las tarjetas del dashboard
        document.getElementById("heartRate").innerHTML =
            `${heart} <small>BPM</small>`;

        document.getElementById("oxygen").innerHTML =
            `${oxygen} <small>%</small>`;

        document.getElementById("sleep").innerHTML =
            `${sleep} <small>H</small>`;

        document.getElementById("activity").innerHTML =
            `${activity} <small>%</small>`;

        // 7. Analizamos los indicadores recibidos
        analyzeHealth(heart, oxygen, sleep);

    } catch (error) {

        // 8. Mostramos el error si falla la comunicación
        console.error("Error de conexión:", error);

        document.getElementById("aiMessage").innerText =
            "No fue posible conectar con el servidor de ASTRA HEALTH AI.";

        document.getElementById("riskStatus").innerText =
            "CONNECTION ERROR";
    }
}


function analyzeHealth(heart, oxygen, sleep) {

    const message = document.getElementById("aiMessage");
    const status = document.getElementById("riskStatus");

    let alerts = [];

    if (heart > 100) {
        alerts.push(
            "Frecuencia cardíaca elevada respecto al umbral ilustrativo."
        );
    }

    if (oxygen < 95) {
        alerts.push(
            "Saturación de oxígeno inferior al umbral ilustrativo."
        );
    }

    if (sleep < 6) {
        alerts.push(
            "Duración de sueño inferior al objetivo de referencia."
        );
    }

    if (alerts.length > 0) {

        status.innerText = "REVIEW REQUIRED";
        status.style.color = "#ffb454";
        status.style.borderColor = "#ffb454";

        message.innerText = alerts.join(" ");

    } else {

        status.innerText = "NO RULE-BASED ALERT";
        status.style.color = "#51e3a2";
        status.style.borderColor = "#51e3a2";

        message.innerText =
            "No se detectaron alertas según las reglas configuradas. Esto no garantiza que el astronauta esté sano.";
    }
}


async function analyzeWithAI() {

    const message = document.getElementById("aiMessage");
    const status = document.getElementById("riskStatus");

    try {

        status.innerText = "ANALYZING...";
        message.innerText = "El modelo está analizando los indicadores.";

        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/health/analyze"
        );

        const result = await response.json();

        if (!response.ok) {
            throw new Error(
                result.detail || "No fue posible analizar los datos."
            );
        }

        const analysis = result.analysis;

        if (analysis.is_anomaly) {

            status.innerText = "UNUSUAL PATTERN";
            status.style.color = "#ffb454";
            status.style.borderColor = "#ffb454";

        } else {

            status.innerText = "USUAL PATTERN";
            status.style.color = "#51e3a2";
            status.style.borderColor = "#51e3a2";
        }

        message.innerText =
            analysis.message +
            " Indicadores más inusuales: " +
            analysis.most_unusual_indicators.join(", ") +
            ". Puntuación: " +
            analysis.anomaly_score;

    } catch (error) {

        console.error("Error en el análisis:", error);

        status.innerText = "AI ANALYSIS ERROR";
        message.innerText = error.message;
    }
}