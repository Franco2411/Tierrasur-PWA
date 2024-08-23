instructions = [
    'SET FOREIGN_KEY_CHECKS=0;',
    'DROP TABLE IF EXISTS usuarios;',
    'SET FOREIGN_KEY_CHECKS=1',
    """
    CREATE TABLE usuarios(
        id INT PRIMARY KEY auto_increment,
        email varchar(50) NOT NULL,
        username varchar(50),
        password varchar(255) NOT NULL
)
    """
]