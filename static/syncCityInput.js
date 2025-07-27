function syncCityInput() {
    const input = document.getElementById('city_input');
    const select = document.getElementById('city_select');
    const options = select.options;

    // Verifica se o texto digitado corresponde a alguma opção no select
    for (let i = 0; i < options.length; i++) {
        if (options[i].text.toLowerCase().includes(input.value.toLowerCase())) {
            select.value = options[i].value; // Define o ID da cidade no select
            return;
        }
    }

    select.value = ""; // Limpa a seleção se não houver correspondência
}

function syncCitySelect() {
    const input = document.getElementById('city_input');
    const select = document.getElementById('city_select');
    input.value = select.options[select.selectedIndex].text; // Define o nome da cidade no input
}