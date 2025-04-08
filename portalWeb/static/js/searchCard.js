document.getElementById('card-input').addEventListener('input', function () {
    const cardName = this.value.trim();
    const cardResult = document.getElementById('div-card-result');

    if (cardName.length > 2) {

        fetch(`/searchCard/${encodeURIComponent(cardName)}/`)
            .then(response => response.json())
            .then(data => {
                cardResult.innerHTML = '';

                if (data.error) {
                    cardResult.innerHTML = `<p style="color:red;">${data.error}</p>`;
                } else if (data.cardNamesList && data.cardNamesList.length > 0) {
                    cardResult.removeAttribute('hidden');
                    const ul = document.createElement('ul');
                    data.cardNamesList.forEach(name => {
                        const li = document.createElement('li');
                        li.textContent = name;
                        ul.appendChild(li);
                    });
                    cardResult.appendChild(ul);
                } else {
                    cardResult.removeAttribute('hidden');
                    cardResult.innerHTML = `<p>Not a single card was found!</p>`;
                }
            })

    } else {
        document.getElementById('div-card-result').innerHTML = '';
        cardResult.setAttribute('hidden');
    }
});