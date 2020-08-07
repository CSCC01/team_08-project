import { environment } from '../../../environments/environment';
import { Component, OnInit, Input } from '@angular/core';
import * as mapboxgl from 'mapbox-gl';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements OnInit {
  @Input() restaurants: any;
  @Input() userId: string;
  @Input() role: string;

  lat = 43.7839;
  lng = -79.1874;

  constructor() {}

  ngOnInit() {
    var options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    };

    Object.getOwnPropertyDescriptor(mapboxgl, 'accessToken').set(
      environment.mapbox.accessToken
    );

    navigator.geolocation.getCurrentPosition(
      (position) => {
        var style = 'mapbox://styles/mapbox/streets-v11';
        var map: mapboxgl.Map;

        map = new mapboxgl.Map({
          container: 'map',
          style: style,
          zoom: 13,
          center: [position.coords.longitude, position.coords.latitude],
        });

        // Add map controls
        map.addControl(new mapboxgl.NavigationControl());

        // Add map markers
        var marker = new mapboxgl.Marker({ color: '#0000FF' })
          .setLngLat([position.coords.longitude, position.coords.latitude])
          .setPopup(new mapboxgl.Popup().setHTML('<p>You are here!</p>'))
          .addTo(map);

        for (var i = 0; i < this.restaurants.length; i++) {
          var index = this.restaurants[i];
          var GEOJson = JSON.parse(index.GEO_location.replace(/\'/g, '"'));

          if (index.GEO_location != 'blank' && GEOJson.long != undefined) {
            var marker = new mapboxgl.Marker({ color: '#165788' })
              .setLngLat([GEOJson.long, GEOJson.lat])
              .setPopup(
                new mapboxgl.Popup().setHTML(
                  `<h2>${index.name}</h2>
                  ${index.address}
                  <br/>
                  ${index.phone}
                  <br/>
                  ${index.cuisine}
                  <br/>
                  <a class="btn" href="${environment.site_url}/restaurant?restaurantId=${index._id}&userId=${this.userId}&role=${this.role}"> View Restaurant </a>`
                )
              )
              .addTo(map);
          }
        }
      },
      this.error,
      options
    );
  }

  error(err) {}
}
