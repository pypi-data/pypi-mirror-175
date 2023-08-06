import{b as o,d as i,p as t,n as s,s as e,y as a,U as n,j as l}from"./index-b34b7b0b.js";import"./c.335cf0f7.js";import"./c.9cb2e71a.js";let c=class extends e{render(){const o=void 0===this._valid?"":this._valid?"✅":"❌";return a`
      <esphome-process-dialog
        .heading=${`Validate ${this.configuration} ${o}`}
        .type=${"validate"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Install"
          @click=${this._openInstall}
        ></mwc-button>
      </esphome-process-dialog>
    `}_openEdit(){n(this.configuration)}_openInstall(){l(this.configuration)}_handleProcessDone(o){this._valid=0==o.detail}_handleClose(){this.parentNode.removeChild(this)}};o([i()],c.prototype,"configuration",void 0),o([t()],c.prototype,"_valid",void 0),c=o([s("esphome-validate-dialog")],c);
