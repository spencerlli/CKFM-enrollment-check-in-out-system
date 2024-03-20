# CKFM-enrollment-check-in-out-system

## Project structure
```
.
├── AttendancePro
│   ├── flask_templates             # Front-end web pages
│   │   ├── admin
│   │   ├── forms
│   │   ├── general
│   │   ├── guardian
│   │   ├── scanner
│   │   └── teacher
│   └── static
│       ├── amis                    # amis SDK
│       └── lib            
│           ├── badge_template.lbx  # Name badge template
│           └── bpac.js             # Printer SDK
└── Backend
    ├── backup
    ├── nginx
    ├── restful_api
    ├── routing_app
    └── test_api
```

## Useful links
Front-end framework：[amis](https://baidu.github.io/amis/)
- [docs](https://baidu.github.io/amis/)
- [repo](https://github.com/baidu/amis)

Required for printing:
- [Printer Driver](https://support.brother.com/g/b/downloadtop.aspx?c=us&lang=en&prod=lpql800eus)
- [b-PAC Client Component](https://support.brother.com/g/s/es/dev/en/bpac/download/index.html?c=eu_ot&lang=en&navi=offall&comple=on&redirect=on)
- [b-PAC Web Extension](https://chrome.google.com/webstore/detail/brother-b-pac-extension/ilpghlfadkjifilabejhhijpfphfcfhb)
