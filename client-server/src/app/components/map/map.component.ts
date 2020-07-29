import { environment } from '../../../environments/environment';
import { Component, OnInit, Input } from '@angular/core';
import * as mapboxgl from 'mapbox-gl';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss'],
})
export class MapComponent implements OnInit {
  @Input() restaurants: any;
  @Input() userId: string;
  @Input() role: string;
  popupDetails: any[] = [];

  map: mapboxgl.Map;
  style = 'mapbox://styles/mapbox/streets-v11';
  lat = 43.7839;
  lng = -79.1874;

  constructor(private route: ActivatedRoute, private router: Router) {}

  ngOnInit() {
    Object.getOwnPropertyDescriptor(mapboxgl, 'accessToken').set(
      environment.mapbox.accessToken
    );
    this.map = new mapboxgl.Map({
      container: 'map',
      style: this.style,
      zoom: 13,
      center: [this.lng, this.lat],
    });
    // Add map controls
    this.map.addControl(new mapboxgl.NavigationControl());

    // Add map markers
    var marker = new mapboxgl.Marker({ color: '#FF0000' })
      .setLngLat([this.lng, this.lat])
      .setPopup(new mapboxgl.Popup().setHTML('<p>You are here!</p>'))
      .addTo(this.map);

    for (var i = 0; i < this.restaurants.length; i++) {
      var index = this.restaurants[i];
      var long = index.GEO_location.substring(
        2,
        index.GEO_location.indexOf("'", 2)
      );
      console.log(
        index.GEO_location.indexOf("'", index.GEO_location.indexOf("'", 2) + 4)
      );
      var lati = index.GEO_location.substring(
        index.GEO_location.indexOf("'", 2) + 2,
        index.GEO_location.indexOf("'", index.GEO_location.indexOf("'", 2) + 2)
      );
      if (index.GEO_location != 'blank' || long != '{"') {
        var marker = new mapboxgl.Marker({ color: '#CB1E21' })
          .setLngLat([+long, this.lat])
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
          .addTo(this.map);
      }
    }
  }
}
