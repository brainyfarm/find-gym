console.log("WTF")

$(document).ready((ready) => {
    console.log(ready);
    if(navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        // Show the user a form to enter location manually

    }

    const showPosition = (position) =>  {
        console.log(position.coords.latitude, position.coords.longitude);
    }
})