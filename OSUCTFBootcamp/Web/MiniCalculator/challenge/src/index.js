const express = require('express')
const cors = require('cors')

const app = express()

app.use(cors())
app.use(express.static('dist'))
app.use('/api', require('./api'))

app.listen(8081, () => {
  console.log('Listening')
})
