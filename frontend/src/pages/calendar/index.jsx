import React, { useState, useEffect } from 'react';
import Header from '../../components/navigation/Header';


import CalendarGrid from './components/CalendarGrid';
import EventSidebar from './components/EventSidebar';
import ViewToolbar from './components/ViewToolbar';

const Calendar = () => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [viewMode, setViewMode] = useState('month');
  const [eventFilters, setEventFilters] = useState({
    tvReleases: true,
    movieReleases: true,
    downloads: true,
    views: true
  });
  const [events, setEvents] = useState([]);
  const [selectedDateEvents, setSelectedDateEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for calendar events
  useEffect(() => {
    const mockEvents = [
    {
      id: 1,
      title: 'The Last of Us',
      type: 'tv',
      eventType: 'release',
      releaseDate: '2026-02-15',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_1c2cd9b43-1764866820820.png",
      imageAlt: 'The Last of Us poster showing Joel and Ellie in post-apocalyptic setting',
      episode: 'S02E03 - Long, Long Time',
      status: 'monitored'
    },
    {
      id: 2,
      title: 'Dune: Part Two',
      type: 'movie',
      eventType: 'download',
      releaseDate: '2026-02-15',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_12de53064-1764683396980.png",
      imageAlt: 'Dune Part Two poster featuring Paul Atreides in desert landscape',
      status: 'downloading',
      progress: 65
    },
    {
      id: 3,
      title: 'Breaking Bad',
      type: 'tv',
      eventType: 'view',
      releaseDate: '2026-02-14',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_14e222417-1766936577311.png",
      imageAlt: 'Breaking Bad poster with Walter White in yellow hazmat suit',
      episode: 'S05E14 - Ozymandias',
      status: 'available',
      viewedBy: 'John Doe'
    },
    {
      id: 4,
      title: 'Oppenheimer',
      type: 'movie',
      eventType: 'view',
      releaseDate: '2026-02-14',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_118ee805e-1767109528627.png",
      imageAlt: 'Oppenheimer poster showing J. Robert Oppenheimer with atomic explosion background',
      status: 'available',
      viewedBy: 'Jane Smith'
    },
    {
      id: 5,
      title: 'House of the Dragon',
      type: 'tv',
      eventType: 'release',
      releaseDate: '2026-02-16',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_153987c15-1767490885175.png",
      imageAlt: 'House of the Dragon poster featuring Targaryen dragons and royal family',
      episode: 'S02E05 - Regent',
      status: 'monitored'
    },
    {
      id: 6,
      title: 'The Batman',
      type: 'movie',
      eventType: 'download',
      releaseDate: '2026-02-17',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_1b1816bc0-1767897110215.png",
      imageAlt: 'The Batman poster showing Batman in dark Gotham City setting',
      status: 'downloading',
      progress: 32
    },
    {
      id: 7,
      title: 'Stranger Things',
      type: 'tv',
      eventType: 'release',
      releaseDate: '2026-02-18',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_18fc9d2c2-1770494626079.png",
      imageAlt: 'Stranger Things poster with main cast and Upside Down imagery',
      episode: 'S05E02 - The Dive',
      status: 'monitored'
    },
    {
      id: 8,
      title: 'Avatar: The Way of Water',
      type: 'movie',
      eventType: 'view',
      releaseDate: '2026-02-12',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_1505dcc4e-1765129194421.png",
      imageAlt: 'Avatar The Way of Water poster featuring Jake Sully and Neytiri underwater',
      status: 'available',
      viewedBy: 'Mike Johnson'
    },
    {
      id: 9,
      title: 'The Mandalorian',
      type: 'tv',
      eventType: 'release',
      releaseDate: '2026-02-19',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_1d1ab121b-1769192219697.png",
      imageAlt: 'The Mandalorian poster showing armored bounty hunter with Grogu',
      episode: 'S04E01 - The Apostate',
      status: 'monitored'
    },
    {
      id: 10,
      title: 'Guardians of the Galaxy Vol. 3',
      type: 'movie',
      eventType: 'download',
      releaseDate: '2026-02-20',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_17014b137-1766958809777.png",
      imageAlt: 'Guardians of the Galaxy Vol 3 poster with team in colorful space setting',
      status: 'available'
    },
    {
      id: 11,
      title: 'The Crown',
      type: 'tv',
      eventType: 'view',
      releaseDate: '2026-02-13',
      imageUrl: "https://images.unsplash.com/photo-1662733853632-00c3fd65d53e",
      imageAlt: 'The Crown poster featuring Queen Elizabeth II in royal regalia',
      episode: 'S06E08 - Sleep, Dearie Sleep',
      status: 'available',
      viewedBy: 'Sarah Williams'
    },
    {
      id: 12,
      title: 'Spider-Man: Across the Spider-Verse',
      type: 'movie',
      eventType: 'release',
      releaseDate: '2026-02-21',
      imageUrl: "https://img.rocket.new/generatedImages/rocket_gen_img_1806ce35b-1768651420798.png",
      imageAlt: 'Spider-Man Across the Spider-Verse poster with Miles Morales swinging through multiverse',
      status: 'monitored'
    }];


    setEvents(mockEvents);
    setIsLoading(false);
  }, []);

  // Update selected date events when date or filters change
  useEffect(() => {
    const filteredEvents = getEventsForDate(selectedDate);
    setSelectedDateEvents(filteredEvents);
  }, [selectedDate, events, eventFilters]);

  const getEventsForDate = (date) => {
    return events?.filter((event) => {
      const eventDate = new Date(event?.releaseDate);
      const matchesDate = eventDate?.getDate() === date?.getDate() &&
      eventDate?.getMonth() === date?.getMonth() &&
      eventDate?.getFullYear() === date?.getFullYear();

      if (!matchesDate) return false;

      // Apply event type filters
      if (event?.eventType === 'release' && event?.type === 'tv' && !eventFilters?.tvReleases) return false;
      if (event?.eventType === 'release' && event?.type === 'movie' && !eventFilters?.movieReleases) return false;
      if (event?.eventType === 'download' && !eventFilters?.downloads) return false;
      if (event?.eventType === 'view' && !eventFilters?.views) return false;

      return true;
    });
  };

  const navigateMonth = (direction) => {
    const newDate = new Date(selectedDate);
    newDate?.setMonth(newDate?.getMonth() + direction);
    setSelectedDate(newDate);
  };

  const goToToday = () => {
    setSelectedDate(new Date());
  };

  const monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-6 md:py-8">
        {/* Page Header */}
        <div className="mb-6">
          <h1 className="text-2xl md:text-3xl font-bold text-foreground mb-2">
            Media Calendar
          </h1>
          <p className="text-muted-foreground">
            Track TV show releases, movie downloads, and viewing activity across your media services
          </p>
        </div>

        {/* View Toolbar */}
        <ViewToolbar
          viewMode={viewMode}
          setViewMode={setViewMode}
          eventFilters={eventFilters}
          setEventFilters={setEventFilters}
          selectedDate={selectedDate}
          monthNames={monthNames}
          navigateMonth={navigateMonth}
          goToToday={goToToday} />
        

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Calendar Grid */}
          <div className="lg:col-span-2">
            <CalendarGrid
              selectedDate={selectedDate}
              setSelectedDate={setSelectedDate}
              events={events}
              eventFilters={eventFilters}
              viewMode={viewMode}
              isLoading={isLoading} />
            
          </div>

          {/* Event Sidebar */}
          <div className="lg:col-span-1">
            <EventSidebar
              selectedDate={selectedDate}
              events={selectedDateEvents}
              isLoading={isLoading} />
            
          </div>
        </div>
      </main>
    </div>);

};

export default Calendar;