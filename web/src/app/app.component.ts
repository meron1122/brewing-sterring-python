import { Component, OnInit } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { IStatus } from 'src/shared/models/istatus';
import { ToastrService } from 'ngx-toastr';
import { setTheme } from 'ngx-bootstrap/utils';
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  myWebSocket: WebSocketSubject<any> = webSocket('ws://192.168.1.144:8765');
  status: Partial<IStatus>;
  setpoint: any;

  constructor(private toastr: ToastrService) {

    setTheme('bs4');
  }

  ngOnInit(): void {
    setInterval(() => this.myWebSocket.next({command: 'get_status'}), 200);

    this.myWebSocket.subscribe(
      (status: IStatus) => {
        this.status = status;
      },
      err => console.log(err)
   );
  }

  public sendSetpoint(){
    if (this.setpoint){
      this.myWebSocket.next({command: 'set_setpoint', arg: this.setpoint});
      }else {
        this.toastr.error('Wpisz najpierw temperaturę!');
      }
    }

  public sendPaddle(state: boolean){
    this.myWebSocket.next({command: 'set_paddle', arg: state});
  }
}
