window.onload = () => {
    $('#basket_ajax_block').on('click', 'input[type="number"]', () => {
        const url = `/baskets/edit/${event.target.name}/${event.target.value}/`;
        $.ajax({
            url: url,
            success: (data) => {
                $('#basket_ajax_block').html(data.result);
            }
        });
    event.preventDefault();
    });
}