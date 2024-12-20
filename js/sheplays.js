function toggleAccordion(event) {
    const allContents = document.querySelectorAll('.accordion-content');
    const itemButton = event.target;
    const itemContent = itemButton.nextElementSibling;

    // Primero, cerrar todos los contenidos abiertos, excepto el actual
    allContents.forEach(content => {
        if (content !== itemContent) {
            content.classList.remove('expanded');
        }
    });

    // Alternar la clase 'expanded' del contenido actual
    itemContent.classList.toggle('expanded');
}