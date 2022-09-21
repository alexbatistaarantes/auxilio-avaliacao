/* Criando a ferramenta de seleção na página */
var st = document.getElementById('selection-tool');
var resize = new Croppie(st, {
    viewport: { width: 100, height: 100 },
    boundary: { width: 500, height: 500 },
    showZoomer: false,
    enableResize: true,
    enableOrientation: true,
    mouseWheelZoom: 'ctrl'
});
resize.bind({
    url: imageUrl,
    points: [0, 0, 200, 100]
});

/* Evento para toda alteração feita na seleção */
st.addEventListener('update', () => {
    const { points } = resize.get();
    const [x1, y1, x2, y2] = points;

    const form = document.querySelector('form');
    /* Insere coordenadas dos pontos no formulário */
    form.querySelector('input#id_x1').value = x1;
    form.querySelector('input#id_y1').value = y1;
    form.querySelector('input#id_x2').value = x2;
    form.querySelector('input#id_y2').value = y1;

    /* Salva a imagem da seleção em base64 no formulário */
    form.querySelector('input#submit').disabled = true;
    resize.result({type: 'base64', size: 'original'})
    .then((image_base64) => {
        form.querySelector('input#submit').disabled = false;
        form.querySelector('input#image_base64').value = image_base64;
    });
});
