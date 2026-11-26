let currentFigure = null;
const uploadForm = document.getElementById("uploadForm");

uploadForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const file = document.getElementById("fileInput").files[0];

    const formData = new FormData();

    formData.append("file", file);

    document.getElementById("loading").style.display = "block";

    document.getElementById("message").innerHTML = "";

    document.getElementById("schemaSection").style.display = "none";

    document.getElementById("promptResult").innerHTML = "";
    document.getElementById("chartContainer").innerHTML = "";

    
    try {

        const response = await fetch("/upload", {

            method: "POST",

            body: formData

        });

        const data = await response.json();
        console.log(data);

        document.getElementById("loading").style.display = "none";

        if (!response.ok) {

            document.getElementById("message").innerHTML =
                `<div class="alert alert-danger">${data.detail}</div>`;

            return;

        }

        document.getElementById("message").innerHTML =
            `<div class="alert alert-success">${data.message}</div>`;

        document.getElementById("schemaSection").style.display = "block";

        document.getElementById("previewSection").style.display = "block";

        document.getElementById("visualizationSection").style.display = "block";

        document.getElementById("rows").textContent = data.schema.rows;

        document.getElementById("columns").textContent = data.schema.columns;

        document.getElementById("columnNames").textContent =
            data.schema.column_names.join(", ");

        let dataTypes = "";

        for (const column in data.schema.data_types) {

            dataTypes += `${column}: ${data.schema.data_types[column]} | `;

        }

        document.getElementById("dataTypes").textContent = dataTypes;

        createPreviewTable(data.preview);

        generateSamplePrompts(
            data.schema.column_names,
            data.schema.data_types
        );
    }

    catch (error) {

        document.getElementById("loading").style.display = "none";

        document.getElementById("message").innerHTML =
            `<div class="alert alert-danger">
                Server Error. Please try again.
            </div>`;

        console.error(error);

    }

});

function createPreviewTable(preview) {

    const table = document.getElementById("previewTable");

    table.innerHTML = "";

    if (preview.length === 0) {

        table.innerHTML =
            "<tr><td>No data available.</td></tr>";

        return;

    }

    const columns = Object.keys(preview[0]);

    let header = "<thead><tr>";

    columns.forEach(column => {

        header += `<th>${column}</th>`;

    });

    header += "</tr></thead>";

    let body = "<tbody>";

    preview.forEach(row => {

        body += "<tr>";

        columns.forEach(column => {

            body += `<td>${row[column]}</td>`;

        });

        body += "</tr>";

    });

    body += "</tbody>";

    table.innerHTML = header + body;

}

function generateSamplePrompts(columns, dataTypes) {

    const samplePrompts = document.getElementById("samplePrompts");

    let numericColumns = [];
    let categoricalColumns = [];

    for (const column of columns) {

        const type = dataTypes[column];

        if (
            type.includes("int") ||
            type.includes("float")
        ) {
            numericColumns.push(column);
        } else {
            categoricalColumns.push(column);
        }
    }

    let prompts = [];

    // Bar chart
    if (numericColumns.length > 0 && categoricalColumns.length > 0) {

        prompts.push(
            `Create a bar chart of ${numericColumns[0]} by ${categoricalColumns[0]}`
        );

    }

    // Average bar chart
    if (numericColumns.length > 0 && categoricalColumns.length > 0) {

        prompts.push(
            `Create a bar chart of average ${numericColumns[0]} by ${categoricalColumns[0]}`
        );

    }

    // Scatter chart
    if (numericColumns.length >= 2) {

        prompts.push(
            `Create a scatter chart of ${numericColumns[0]} by ${numericColumns[1]}`
        );

    }

    // Line chart
    if (numericColumns.length > 0 && categoricalColumns.length > 0) {

        prompts.push(
            `Create a line chart of ${numericColumns[0]} by ${categoricalColumns[0]}`
        );

    }

    // Pie chart
    if (numericColumns.length > 0 && categoricalColumns.length > 0) {

        prompts.push(
            `Create a pie chart of ${numericColumns[0]} by ${categoricalColumns[0]}`
        );

    }

    // Histogram
    if (numericColumns.length > 0) {

        prompts.push(
            `Create a histogram of ${numericColumns[0]}`
        );

    }

    if (prompts.length === 0) {

        samplePrompts.innerHTML = "";

        return;
    }

    let html = `
        <p class="text-muted mb-2">
            💡 Try these sample prompts:
        </p>
    `;

    prompts.forEach(prompt => {

        html += `
            <button
                type="button"
                class="btn btn-outline-primary btn-sm m-1 sample-prompt"
                data-prompt="${prompt}">
                ${prompt}
            </button>
        `;

    });

    samplePrompts.innerHTML = html;

    document.querySelectorAll(".sample-prompt").forEach(button => {

        button.addEventListener("click", function () {

            document.getElementById("promptInput").value =
                this.dataset.prompt;

        });

    });
}

const promptForm = document.getElementById("promptForm");

promptForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const prompt = document.getElementById("promptInput").value;

    try {

        const response = await fetch("/visualize", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                prompt: prompt
            })

        });

        const data = await response.json();

        if (!response.ok) {

            document.getElementById("promptResult").innerHTML =
                `<div class="alert alert-danger">${data.detail}</div>`;

            return;

        }

document.getElementById("promptResult").innerHTML = `

<div class="alert alert-info">

    <h5>Prompt Parsed Successfully</h5>

    <p><strong>Original Prompt:</strong> ${data.parsed_prompt.original_prompt}</p>

    <p><strong>Chart Type:</strong> ${data.parsed_prompt.chart_type}</p>

    <p><strong>X-Axis:</strong> ${data.parsed_prompt.x_axis ?? "Not Detected"}</p>

    <p><strong>Y-Axis:</strong> ${data.parsed_prompt.y_axis ?? "Not Detected"}</p>

    <p><strong>Aggregation:</strong> ${data.parsed_prompt.aggregation ?? "None"}</p>

</div>

`;

const figure = JSON.parse(data.figure);

currentFigure = figure;

document.getElementById("downloadHtmlBtn").style.display = "inline-block";

Plotly.newPlot(
    "chartContainer",
    figure.data,
    figure.layout,
    {
        responsive: true
    }
);

    }

    catch (error) {

        document.getElementById("promptResult").innerHTML =
            `<div class="alert alert-danger">
                Failed to process visualization request.
            </div>`;

        console.error(error);

    }

});

document.getElementById("downloadHtmlBtn").addEventListener("click", function () {

    if (!currentFigure) {
        return;
    }

    Plotly.downloadImage(
    currentFigure,
    {
        format: "png",
        filename: "visualization",
        width: 1200,
        height: 700
    }
);

});