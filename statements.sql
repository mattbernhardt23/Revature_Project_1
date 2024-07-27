-- Create the Bookstore
CREATE DATABASE book_store;
USE book_store;
-- Create the Product Table
CREATE TABLE inventory (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    year_published INT,
    description TEXT,
    sales_price DECIMAL(10, 2) NOT NULL,
    product_cost DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
);
-- Create an Order Table
CREATE TABLE orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    product_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (username) REFERENCES customers(username),
    FOREIGN KEY (product_id) REFERENCES inventory(product_id)
);
-- Create a Customer Table 
CREATE TABLE customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    admin BOOLEAN DEFAULT FALSE,
    account_balance DECIMAL(10, 2) NOT NULL DEFAULT 0
);

-- Add Inventory
INSERT into book_inventory (
    title, 
    author, 
    year_published, 
    description, 
    sales_price, 
    product_cost, 
    stock_quantity
    ) VALUES 
('Money Ball', 'Michael Lewis', 2003, 'Moneyball: The Art of Winning an Unfair Game is a book by Michael Lewis, published in 2003, about the Oakland Athletics baseball team and its general manager Billy Beane. Its focus is the team''s analytical, evidence-based, sabermetric approach to assembling a competitive baseball team despite Oakland''s small budget.', 14.99, 7.00, 100),
('The Big Short', 'Michael Lewis', 2010, 'The Big Short: Inside the Doomsday Machine is a non-fiction book by Michael Lewis about the build-up of the United States housing bubble during the 2000s. The book was released on March 15, 2010, by W. W. Norton & Company. It spent 28 weeks on The New York Times best-seller list.', 14.99, 7.00, 100),
('Liar''s Poker', 'Michael Lewis', 1989, 'Liar''s Poker is a non-fiction, semi-autobiographical book by Michael Lewis describing the author''s experiences as a bond salesman on Wall Street during the late 1980s. First published in 1989, it is considered one of the books that defined Wall Street during the 1980s, along with Bryan Burrough and John Helyar''s Barbarians at the Gate: The Fall of RJR Nabisco, and the fictional The Bonfire of the Vanities by Tom Wolfe.', 14.99, 7.00, 100),
('Going Infinite', 'Michael Lewis', 2021, 'Going Infinite is a book by Michael Lewis about the rise and fall of Sam Bankman-Fried and the crypto-exchanage FTX.', 14.99, 7.00, 10),
('The Intelligent Investor', 'Benjamin Graham', 1949, 'The Intelligent Investor by Benjamin Graham, first published in 1949, is a widely acclaimed book on value investing. The book teaches readers strategies on how to successfully use value investing in the stock market.', 14.99, 7.00, 100),
('The Essays of Warren Buffett', 'Warren Buffett', 1997, 'The Essays of Warren Buffett: Lessons for Corporate America is a collection of Warren Buffett''s writings on business, finance, and investing. Taken from his letters to Berkshire Hathaway shareholders, these letters have become an annual required read for investors.', 14.99, 7.00, 100),
('Zen Mind Beginner''s Mind', 'Shunryu Suzuki', 1970, 'Zen Mind, Beginner''s Mind by the late Shunryu Suzuki is a book of instruction about how to practice Zen, about Zen life, and about the attitudes and understanding that make Zen practice possible. Suzuki Roshi presents the basics—from the details of posture and breathing in zazen to the perception of nonduality—in a way that is not only remarkably clear, but that also resonates with the joy of insight from the first to the last page.', 9.99, 5.00, 100),
('The Art of War', 'Sun Tzu', 0, 'The Art of War is an ancient Chinese military treatise dating from the Late Spring and Autumn Period. The work, which is attributed to the ancient Chinese military strategist Sun Tzu, is composed of 13 chapters. Each one is devoted to an aspect of warfare and how it applies to military strategy and tactics.', 9.99, 5.00, 100),
('The Making of the Atomic Bomb', 'Richard Rhodes', 1986, 'The Making of the Atomic Bomb is a contemporary history book written by the American journalist and historian Richard Rhodes, first published by Simon & Schuster in 1986. It won the Pulitzer Prize for General Non-Fiction, the National Book Award for Nonfiction, and a National Book Critics Circle Award.', 14.99, 7.00, 100),
('The Power Broker', 'Robert Caro', 1974, 'The Power Broker: Robert Moses and the Fall of New York is a 1974 biography of Robert Moses by Robert Caro. The book focuses on the creation and use of power in local and state politics, as witnessed through Moses'' use of unelected positions to design and implement dozens of highways and bridges, sometimes at great cost to the communities he nominally served.', 14.99, 7.00, 100),
('Titan', 'Ron Chernow', 1998, 'Titan: The Life of John D. Rockefeller, Sr. is a biography of John D. Rockefeller, written by Ron Chernow. It was published in 1998 by Random House. The book is 774 pages long, and as of 2012, it has been printed in 14 editions.', 14.99, 7.00, 100),
('The Innovators', 'Walter Isaacson', 2014, 'The Innovators: How a Group of Hackers, Geniuses, and Geeks Created the Digital Revolution is an overview of the history of computer science and the Digital Revolution. It was written by Walter Isaacson, and published in 2014 by Simon & Schuster.', 14.99, 7.00, 100),
('Steve Jobs', 'Walter Isaacson', 2011, 'Steve Jobs is the authorized self-titled biography of Steve Jobs. The book was written at the request of Jobs by Walter Isaacson, a former executive at CNN and TIME who has written best-selling biographies of Benjamin Franklin and Albert Einstein.', 14.99, 7.00, 100),
('Benjamin Franklin: An American Life', 'Walter Isaacson', 2003, 'Benjamin Franklin: An American Life is a non-fiction book authored by Walter Isaacson. It is a biography of Benjamin Franklin. The book was published in 2003 by Simon & Schuster.', 14.99, 7.00, 100),
('Einstein: His Life and Universe', 'Walter Isaacson', 2007, 'Einstein: His Life and Universe is a biography written by Walter Isaacson about the life of the physicist Albert Einstein. The book was released in April 2007 and is published by Simon & Schuster.', 14.99, 7.00, 100),
('Leonardo da Vinci', 'Walter Isaacson', 2017, 'Leonardo da Vinci is a biography of the Italian Renaissance polymath Leonardo da Vinci written by Walter Isaacson. The book has been described as "an engrossing profile of the world''s most famous artist" and as "a portrait of a creative genius who lived at a time when art, science, and engineering were beginning to come together."', 14.99, 7.00, 100),
('The Body Keeps Score', 'Bessel van der Kolk', 2014, 'The Body Keeps the Score: Brain, Mind, and Body in the Healing of Trauma is a 2014 book by Bessel van der Kolk about the effects of psychological trauma, also known as traumatic stress. The book describes van der Kolk''s research and experiences as the founder and medical director of the Trauma Center in Brookline, Massachusetts.', 14.99, 7.00, 100),
('The Untethered Soul', 'Michael Singer', 2007, 'The Untethered Soul: The Journey Beyond Yourself is a 2007 self-help book by spiritual teacher Michael A. Singer. The book aims to help readers find inner peace by working on their consciousness.', 14.99, 7.00, 100),
('The Four Agreements', 'Don Miguel Ruiz', 1997, 'The Four Agreements: A Practical Guide to Personal Freedom is a self-help book by bestselling author Don Miguel Ruiz with Janet Mills. The book offers a code of personal conduct based on ancient Toltec wisdom that advocates freedom from self-limiting beliefs that may cause suffering and limitation in a person''s life.', 14.99, 7.00, 100),
('The 7 Habits of Highly Effective People', 'Stephen Covey', 1989, 'The 7 Habits of Highly Effective People, first published in 1989, is a business and self-help book written by Stephen Covey. Covey presents an approach to being effective in attaining goals by aligning oneself to what he calls "true north" principles based on a character ethic that he presents as universal and timeless.', 14.99, 7.00, 100),
('Outliers', 'Malcolm Gladwell', 2008, 'Outliers: The Story of Success is the third non-fiction book written by Malcolm Gladwell and published by Little, Brown and Company on November 18, 2008. In Outliers, Gladwell examines the factors that contribute to high levels of success.', 14.99, 7.00, 100),
('Blink', 'Malcolm Gladwell', 2005, 'Blink: The Power of Thinking Without Thinking is Malcolm Gladwell''s second book. It presents in popular science format research from psychology and behavioral economics on the adaptive unconscious: mental processes that work rapidly and automatically from relatively little information.', 14.99, 7.00, 100),
('The Tipping Point', 'Malcolm Gladwell', 2000, 'The Tipping Point: How Little Things Can Make a Big Difference is the debut book by Malcolm Gladwell, first published by Little, Brown in 2000. Gladwell defines a tipping point as "the moment of critical mass, the threshold, the boiling point".', 14.99, 7.00, 100),
('David and Goliath', 'Malcolm Gladwell', 2013, 'David and Goliath: Underdogs, Misfits, and the Art of Battling Giants is a non-fiction book written by Malcolm Gladwell and published by Little, Brown and Company on October 1, 2013. The book focuses on the probability of improbable events occurring in situations where one outcome is greatly favored over the other.', 14.99, 7.00, 100),
('Napoleon', 'Andrew Roberts', 2014, 'Napoleon: A Life is a biography of Napoleon Bonaparte written by Andrew Roberts and published by Viking Press in 2014. The book is 976 pages, including notes and index, and it has been well received by critics.', 14.99, 7.00, 100),
('Zen and the Art of Motorcycle Maintenance', 'Robert Pirsig', 1974, 'Zen and the Art of Motorcycle Maintenance: An Inquiry into Values is a book by Robert M. Pirsig first published in 1974. It is a work of fictionalized autobiography, and is the first of Pirsig''s texts in which he explores his Metaphysics of Quality.', 14.99, 7.00, 100),
('Entangled Life', 'Merlin Sheldrake', 2020, 'Entangled Life: How Fungi Make Our Worlds, Change Our Minds, and Shape Our Futures is a 2020 non-fiction book by Merlin Sheldrake. The book explores the role of fungi in the world, and the potential uses of fungi in various fields.', 14.99, 7.00, 100),
('The Lean Startup', 'Eric Ries', 2011, 'The Lean Startup: How Today''s Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses is a book by Eric Ries describing his proposed lean startup strategy for startup companies.', 14.99, 7.00, 100),
('The 48 Laws of Power', 'Robert Greene', 1998, 'The 48 Laws of Power is a practical guide for anyone who wants power, observes power, or wants to arm themselves against power. Written by Robert Greene and first published in 1998, it is often praised for its practicality and its focus on the laws of power that can be used in everyday life.', 14.99, 7.00, 100),
('Mastery', 'Robert Greene', 2012, 'Mastery is the fifth book by the American author Robert Greene. The book examines the lives of historical figures such as Charles Darwin and Henry Ford, as well as the lives of contemporary leaders such as Paul Graham and Freddie Roach, and examines what led to their success.', 14.99, 7.00, 100),
('The 33 Strategies of War', 'Robert Greene', 2006, 'The 33 Strategies of War is a 2006 self-help book by American author Robert Greene that is described as a "guide to the subtle social game of everyday life informed by the military principles in war".', 14.99, 7.00, 100)
;

