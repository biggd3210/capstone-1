
// declare variables
const $find_rooms = $('.view-rooms');

// finding and loading available rooms.
async function load_available_rooms(hotel_id, adults, checkIn, checkOut) {
    
    const data = {
        "hotelIds": hotel_id,
        "adults": adults,
        "checkInDate": checkIn,
        "checkOutDate": checkOut
    }
    const res = await axios.post('/hotels/rooms/search', data);
    return res.data;
}

function populate_room_data(room) {
    const db_entry = room;
    $('#checkInDate').text(room['checkInDate']);
    $('#checkOutDate').text(room['checkOutDate']);
    $('#hotelName').text(room['hotelName']);
    $('#adults').text(room['numOfGuests']);
    $('#price').text(room['price']);
    $('#currency').text(room['currency']);
    
    $('#component_info').val(JSON.stringify(db_entry));
}

$find_rooms.on('click', async function(e) {
    e.preventDefault();
    const $hotelId = e.target.value;
    const checkInDate = $('#checkIn').val();
    const checkOutDate = $('#checkOut').val();
    const adults = $('#numAdults').val();
    const rooms = await load_available_rooms($hotelId, adults, checkInDate, checkOutDate);
    
    if (rooms['message']) {
        $('#room-error').show();
        $('#modal-footer').hide();
        $('#modal-body').hide();
    }

    else {
        $('#room-error').hide();
        $('#modal-footer').show();
        $('#modal-body').show();
        populate_room_data(rooms);
    }

    $('#room').modal('toggle');
})

$('#close-modal').on('click', function() {
    $('#room').modal('toggle');
})


// sharing link with external emails

function display_sent_message(message, code) {
    const flash_msg = $('<div id="flash-message-js"></div>')
        .addClass(['alert', `alert-${code}`])
        .text(message)
    $('#flash-share').prepend(flash_msg)
}

function remove_sent_message() {
    $('#flash-message-js').remove();
}


$('#confirm_share').on('click', async function(e) {
    e.preventDefault();

    const data = {
        "from_email": $('#from_email').val(),
        "to_email": $('#to_email').val(),
        "subject": $('#subject').val(),
        "body": $('#body').val(),
        "link": $('#link').val()
    }
    const res = await axios.post('/itineraries/share', data);
    const info = res.data;
    if (info['code'] == 'success') {
        display_sent_message("Message sent successfully!", 'success')
        setTimeout(remove_sent_message, 5000)
    }
    else if (info['code'] == 'danger') {
        display_sent_message("Message failed to send.", 'danger')
        setTimeout(remove_sent_message, 5000)
    }
})

$('#itin_share').on('click', function() {
    $('#itin_share_modal').modal('toggle');
})

$('#cancel_share').on('click', function() {
    $('#itin_share_modal').modal('toggle');
})

$('#close-share-modal').on('click', function() {
    $('#itin_share_modal').modal('toggle');
})