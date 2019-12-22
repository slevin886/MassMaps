const mymap = L.map('mapid').setView([42.338032,-71.211578], 11);
//[42.360960, -71.058200], 1

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    accessToken: 'pk.eyJ1Ijoic2xldmluODg2IiwiYSI6ImNrNGhtZTNneTFiZXczbW83eXgweWVrcXcifQ.vtx-bvQmfcVdM-ZEswS3Sg'
}).addTo(mymap);