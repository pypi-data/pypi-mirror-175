import{b as e,d as o,n as s,s as i,y as t}from"./index-b34b7b0b.js";import"./c.335cf0f7.js";import"./c.9cb2e71a.js";let a=class extends i{render(){return t`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};e([o()],a.prototype,"configuration",void 0),a=e([s("esphome-clean-mqtt-dialog")],a);
