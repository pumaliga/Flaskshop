import {upload} from './adding.js'

upload('#file', {
    multi: true,
    accept: ['.png', '.jpeg', '.jpg']
})