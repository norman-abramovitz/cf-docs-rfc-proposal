'use strict'

// The year of a date written YYYY-MM-DD: {{yearOf page.attributes.last-updated}}
module.exports = (date) => String(date || '').slice(0, 4)
