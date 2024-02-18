const express = require('express');
const port = process.env.PORT || 8000;

const app = express();

app.get('/', (req, res) => {
  res.json({
    message: 'Hello World!'
  });
});

const users = require('./routes/users');
app.use('/users', users);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});