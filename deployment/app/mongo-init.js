const applicationDatabase = db.getSiblingDB('LibreChat');
applicationDatabase.createUser({
  user: 'residentapp',
  pwd: process.env.MONGO_APP_PASSWORD,
  roles: [{ role: 'readWrite', db: 'LibreChat' }],
});
