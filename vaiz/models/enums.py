from enum import Enum


class AvatarMode(int, Enum):
    """
    Enum for avatar modes.
    """
    Uploaded = 0
    Generated = 2


class Icon(str, Enum):
    """
    Enum for styler icons.
    """
    Cursor = 'Cursor'
    Square = 'Square'
    Hexagon = 'Hexagon'
    Rhombus = 'Rhombus'
    Triangle = 'Triangle'
    Checkbox = 'Checkbox'
    Diamonds = 'Diamonds'
    Circle = 'Circle'
    Light = 'Light'
    Search = 'Search'
    Stop = 'Stop'
    User = 'User'
    People = 'People'
    UserGroup2 = 'UserGroup2'
    ConnectedPeople = 'ConnectedPeople'
    Col = 'Col'
    Code = 'Code'
    Todo = 'Todo'
    Board = 'Board'
    Document = 'Document'
    Project = 'Project'
    Air = 'Air'
    Atom = 'Atom'
    Molecule = 'Molecule'
    Battery = 'Battery'
    BatteryCharging = 'BatteryCharging'
    BatteryLevel = 'BatteryLevel'
    BenzeneRing = 'BenzeneRing'
    BGRemover = 'BGRemover'
    Barcode = 'Barcode'
    QR = 'QR'
    Basilica = 'Basilica'
    Basketball = 'Basketball'
    Binoculars = 'Binoculars'
    BlackHat = 'BlackHat'
    Hat = 'Hat'
    Bot = 'Bot'
    Broom = 'Broom'
    CampingChair = 'CampingChair'
    Cable = 'Cable'
    Terminal = 'Terminal'
    Rs232Female = 'Rs232Female'
    CD = 'CD'
    Music = 'Music'
    Music2 = 'Music2'
    MusicPlaylist = 'MusicPlaylist'
    Swap = 'Swap'
    Camera = 'Camera'
    Camera2 = 'Camera2'
    Aperture = 'Aperture'
    Clock = 'Clock'
    Watch = 'Watch'
    Tenses = 'Tenses'
    Voicemail = 'Voicemail'
    WatchesFrontView = 'WatchesFrontView'
    WeddingRings = 'WeddingRings'
    List = 'List'
    Restart = 'Restart'
    Target = 'Target'
    Moon = 'Moon'
    Sun = 'Sun'
    Cloud = 'Cloud'
    Snow = 'Snow'
    Fire = 'Fire'
    Drop = 'Drop'
    DoctorsBag = 'DoctorsBag'
    Hospital = 'Hospital'
    MedicalDoctor = 'MedicalDoctor'
    ELearning = 'ELearning'
    Laptop = 'Laptop'
    FanSpeed = 'FanSpeed'
    MindMap = 'MindMap'
    Mirror = 'Mirror'
    Attach = 'Attach'
    Flag = 'Flag'
    Finish = 'Finish'
    Crown = 'Crown'
    Money = 'Money'
    Coins = 'Coins'
    Shield = 'Shield'
    Trophy = 'Trophy'
    WomanHead = 'WomanHead'
    Knight = 'Knight'
    Bug = 'Bug'
    Bird = 'Bird'
    PeacePigeon = 'PeacePigeon'
    Penguin = 'Penguin'
    Fish = 'Fish'
    Alien = 'Alien'
    Panda = 'Panda'
    Cat = 'Cat'
    Dog = 'Dog'
    Unicorn = 'Unicorn'
    Run = 'Run'
    Swimming = 'Swimming'
    Ball = 'Ball'
    Geography = 'Geography'
    Planet = 'Planet'
    Location = 'Location'
    Navigate = 'Navigate'
    Stormtrooper = 'Stormtrooper'
    SpaceFighter = 'SpaceFighter'
    Submarine = 'Submarine'
    GpsSignal = 'GpsSignal'
    Radio = 'Radio'
    InternetAntenna = 'InternetAntenna'
    Satellites = 'Satellites'
    Satellite = 'Satellite'
    Speed = 'Speed'
    Plane = 'Plane'
    Ship = 'Ship'
    ShipWheel = 'ShipWheel'
    Lifebuoy = 'Lifebuoy'
    Launch = 'Launch'
    Car = 'Car'
    BikePath = 'BikePath'
    Cycling = 'Cycling'
    MotorbikeHelmet = 'MotorbikeHelmet'
    Road = 'Road'
    Video = 'Video'
    Play = 'Play'
    New = 'New'
    Table = 'Table'
    Chart = 'Chart'
    Rename = 'Rename'
    Broadcast = 'Broadcast'
    Sound = 'Sound'
    Info = 'Info'
    Help = 'Help'
    Quote = 'Quote'
    Attention = 'Attention'
    Add = 'Add'
    Percent = 'Percent'
    Percent25 = '25%'
    Percent50 = '50%'
    Thumb = 'Thumb'
    Delete = 'Delete'
    Type = 'Type'
    Asterisk = 'Asterisk'
    Email = 'Email'
    Mail = 'Mail'
    Message = 'Message'
    Image = 'Image'
    Coffee = 'Coffee'
    Heart = 'Heart'
    Star = 'Star'
    Link = 'Link'
    Happy = 'Happy'
    Phone = 'Phone'
    Layers = 'Layers'
    Chat = 'Chat'
    Apps = 'Apps'
    Up = 'Up'
    Lab = 'Lab'
    Cancel = 'Cancel'
    Poo = 'Poo'
    Skull = 'Skull'
    Bone = 'Bone'
    Dice = 'Dice'
    Puzzle = 'Puzzle'
    Bang = 'Bang'
    Explosion = 'Explosion'
    Gun = 'Gun'
    Shower = 'Shower'
    SpaFlower = 'SpaFlower'
    FoamBubbles = 'FoamBubbles'
    Galaxy = 'Galaxy'
    Beer = 'Beer'
    Champagne = 'Champagne'
    WineGlass = 'WineGlass'
    Cocktail = 'Cocktail'
    Plate = 'Plate'
    Bookmark = 'Bookmark'
    Book = 'Book'
    Sent = 'Sent'
    Home = 'Home'
    MarkerPen = 'MarkerPen'
    Illustrator = 'Illustrator'
    Paint = 'Paint'
    Paint2 = 'Paint2'
    Gear = 'Gear'
    BoxClose = 'BoxClose'
    Alpha = 'Alpha'
    Beta = 'Beta'
    Gamma = 'Gamma'
    Lambda = 'Lambda'
    Mu = 'Mu'
    Omega = 'Omega'
    Pi = 'Pi'
    Sigma = 'Sigma'
    TypeText = 'TypeText'
    TypeNumber = 'TypeNumber'
    TypeDate = 'TypeDate'
    TypeCheck = 'TypeCheck'
    TypeUser = 'TypeUser'


class Color(str, Enum):
    """
    Enum for colors.
    """
    Silver = 'silver'
    Red = 'red'
    Orange = 'orange'
    Gold = 'gold'
    Olive = 'olive'
    Green = 'green'
    Mint = 'mint'
    Blue = 'blue'
    Violet = 'violet'
    Lavender = 'lavender'
    Magenta = 'magenta'
    Rose = 'rose'


class UploadFileType(str, Enum):
    """
    Enum for upload file types.
    """
    Image = 'Image'
    File = 'File'
    Video = 'Video'
    Pdf = 'Pdf'


class Kind(str, Enum):
    Space = "Space"
    Project = "Project"
    Task = "Task"
    Document = "Document"
    Board = "Board"
    Milestone = "Milestone"
    Member = "Member"


class CommentReactionType(Enum):
    """Popular emoji reactions for comments."""
    THUMBS_UP = "thumbs_up"
    HEART = "heart"
    LAUGHING = "joy"
    WOW = "open_mouth"
    CRYING = "cry"
    ANGRY = "angry"
    PARTY = "tada"


# Metadata for comment reactions based on emoji-picker-react standards
COMMENT_REACTION_METADATA = {
    CommentReactionType.THUMBS_UP: {
        "id": "1f44d",
        "name": "Thumbs Up Sign",
        "native": "👍",
        "unified": "1f44d",
        "keywords": ["thumbsup", "yes", "awesome", "good", "agree", "accept", "cool", "hand", "like"],
        "shortcodes": ":thumbsup:",
    },
    CommentReactionType.HEART: {
        "id": "2764-fe0f",
        "name": "Red Heart",
        "native": "❤️",
        "unified": "2764-fe0f",
        "keywords": ["love", "like", "affection", "valentines", "infatuation", "crush", "heart"],
        "shortcodes": ":heart:",
    },
    CommentReactionType.LAUGHING: {
        "id": "1f602",
        "name": "Face with Tears of Joy",
        "native": "😂",
        "unified": "1f602",
        "keywords": ["face", "tears", "joy", "laugh", "happy", "funny", "haha", "lol"],
        "shortcodes": ":joy:",
    },
    CommentReactionType.WOW: {
        "id": "1f62e",
        "name": "Face with Open Mouth",
        "native": "😮",
        "unified": "1f62e",
        "keywords": ["face", "surprise", "impressed", "wow", "whoa", "amazed", "gasp"],
        "shortcodes": ":open_mouth:",
    },
    CommentReactionType.CRYING: {
        "id": "1f622", 
        "name": "Crying Face",
        "native": "😢",
        "unified": "1f622",
        "keywords": ["face", "tears", "sad", "depressed", "upset", "cry"],
        "shortcodes": ":cry:",
    },
    CommentReactionType.ANGRY: {
        "id": "1f621",
        "name": "Pouting Face", 
        "native": "😡",
        "unified": "1f621",
        "keywords": ["mad", "face", "annoyed", "frustrated", "pouting", "angry"],
        "shortcodes": ":rage:",
    },
    CommentReactionType.PARTY: {
        "id": "1f389",
        "name": "Party Popper",
        "native": "🎉", 
        "unified": "1f389",
        "keywords": ["party", "congratulations", "birthday", "celebration", "tada"],
        "shortcodes": ":tada:",
    },
} 