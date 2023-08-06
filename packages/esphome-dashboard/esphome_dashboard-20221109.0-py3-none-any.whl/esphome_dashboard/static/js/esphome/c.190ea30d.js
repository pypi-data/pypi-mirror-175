import{D as o,r as e,b as i,d as t,p as a,n,s,y as c,W as d,U as l}from"./index-b34b7b0b.js";import"./c.9cb2e71a.js";let r=class extends s{constructor(){super(...arguments),this._showCopied=!1}render(){return c`
      <mwc-dialog
        open
        heading=${`API key for ${this.configuration}`}
        scrimClickAction
        @closed=${this._handleClose}
      >
        ${void 0===this._apiKey?"Loading…":null===this._apiKey?c`Unable to automatically extract API key. Open the configuration
              and look for <code>api:</code>.`:c`
              <div class="key" @click=${this._copyApiKey}>
                <code>${this._apiKey}</code>
                <mwc-button ?disabled=${this._showCopied}
                  >${this._showCopied?"Copied!":"Copy"}</mwc-button
                >
              </div>
            `}
        ${null===this._apiKey?c`
              <mwc-button
                @click=${this._editConfig}
                no-attention
                slot="secondaryAction"
                dialogAction="close"
                label="Open configuration"
              ></mwc-button>
            `:""}

        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      </mwc-dialog>
    `}firstUpdated(o){super.firstUpdated(o),d(this.configuration).then((async o=>{var e,i;this._apiKey=null===(i=null===(e=null==o?void 0:o.api)||void 0===e?void 0:e.encryption)||void 0===i?void 0:i.key}))}_copyApiKey(){(async o=>{if(navigator.clipboard)try{return void await navigator.clipboard.writeText(o)}catch{}const e=document.createElement("textarea");e.value=o,document.body.appendChild(e),e.select(),document.execCommand("copy"),document.body.removeChild(e)})(this._apiKey),this._showCopied=!0,setTimeout((()=>this._showCopied=!1),2e3)}_editConfig(){l(this.configuration)}_handleClose(){this.parentNode.removeChild(this)}};r.styles=[o,e`
      .key {
        position: relative;
        display: flex;
        align-items: center;
      }
      code {
        word-break: break-all;
      }
      .key mwc-button {
        margin-left: 16px;
      }
      .copied {
        font-weight: bold;
        color: var(--alert-success-color);

        position: absolute;
        background-color: var(--mdc-theme-surface, #fff);
        padding: 10px;
        right: 0;
        font-size: 1.2em;
      }
    `],i([t()],r.prototype,"configuration",void 0),i([a()],r.prototype,"_apiKey",void 0),i([a()],r.prototype,"_showCopied",void 0),r=i([n("esphome-show-api-key-dialog")],r);
