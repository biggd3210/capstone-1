
const $find_rooms = $('.view-rooms')

async function load_available_rooms(hotel_id) {

    const res = await axios.get('/hotels/rooms/search', data={
        "hotelIds": hotel_id,
        "adults": 2
    });

    console.log("res is ", res.data)
}

$find_rooms.on('click', function(e) {
    console.log("e.target is", e.target)
    console.log("e.parent is ", e.parent)
})