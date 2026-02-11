import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import CalendarEvent from './CalendarEvent';

const MiniCalendar = ({ events }) => {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [viewMode, setViewMode] = useState('week'); // 'week' or 'month'

  const getDaysInMonth = (date) => {
    const year = date?.getFullYear();
    const month = date?.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay?.getDate();
    const startingDayOfWeek = firstDay?.getDay();
    
    return { daysInMonth, startingDayOfWeek, year, month };
  };

  const getWeekDays = (date) => {
    const days = [];
    const currentDay = new Date(date);
    currentDay?.setDate(currentDay?.getDate() - currentDay?.getDay());
    
    for (let i = 0; i < 7; i++) {
      days?.push(new Date(currentDay));
      currentDay?.setDate(currentDay?.getDate() + 1);
    }
    
    return days;
  };

  const navigateMonth = (direction) => {
    const newDate = new Date(selectedDate);
    newDate?.setMonth(newDate?.getMonth() + direction);
    setSelectedDate(newDate);
  };

  const navigateWeek = (direction) => {
    const newDate = new Date(selectedDate);
    newDate?.setDate(newDate?.getDate() + (direction * 7));
    setSelectedDate(newDate);
  };

  const isToday = (date) => {
    const today = new Date();
    return date?.getDate() === today?.getDate() &&
           date?.getMonth() === today?.getMonth() &&
           date?.getFullYear() === today?.getFullYear();
  };

  const hasEvents = (date) => {
    return events?.some(event => {
      const eventDate = new Date(event.releaseDate);
      return eventDate?.getDate() === date?.getDate() &&
             eventDate?.getMonth() === date?.getMonth() &&
             eventDate?.getFullYear() === date?.getFullYear();
    });
  };

  const getEventsForDate = (date) => {
    return events?.filter(event => {
      const eventDate = new Date(event.releaseDate);
      return eventDate?.getDate() === date?.getDate() &&
             eventDate?.getMonth() === date?.getMonth() &&
             eventDate?.getFullYear() === date?.getFullYear();
    });
  };

  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];
  const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  const { daysInMonth, startingDayOfWeek, year, month } = getDaysInMonth(selectedDate);
  const weekDays = getWeekDays(selectedDate);
  const selectedDateEvents = getEventsForDate(selectedDate);

  return (
    <div className="bg-card border border-border rounded-lg overflow-hidden">
      <div className="p-4 md:p-6 border-b border-border">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg md:text-xl font-semibold text-foreground">
            Upcoming Releases
          </h2>
          <div className="flex items-center gap-2">
            <Button
              variant={viewMode === 'week' ? 'default' : 'outline'}
              size="xs"
              onClick={() => setViewMode('week')}
            >
              Week
            </Button>
            <Button
              variant={viewMode === 'month' ? 'default' : 'outline'}
              size="xs"
              onClick={() => setViewMode('month')}
            >
              Month
            </Button>
          </div>
        </div>

        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base md:text-lg font-semibold text-foreground">
            {monthNames?.[month]} {year}
          </h3>
          <div className="flex items-center gap-2">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => viewMode === 'week' ? navigateWeek(-1) : navigateMonth(-1)}
              iconName="ChevronLeft"
              iconSize={20}
            />
            <Button
              variant="ghost"
              size="xs"
              onClick={() => setSelectedDate(new Date())}
            >
              Today
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => viewMode === 'week' ? navigateWeek(1) : navigateMonth(1)}
              iconName="ChevronRight"
              iconSize={20}
            />
          </div>
        </div>

        {viewMode === 'week' ? (
          <div className="grid grid-cols-7 gap-1 md:gap-2">
            {dayNames?.map((day) => (
              <div key={day} className="text-center text-xs font-medium text-muted-foreground py-2">
                {day}
              </div>
            ))}
            {weekDays?.map((date, index) => {
              const dayEvents = getEventsForDate(date);
              const isSelected = date?.getDate() === selectedDate?.getDate() &&
                               date?.getMonth() === selectedDate?.getMonth();
              
              return (
                <button
                  key={index}
                  onClick={() => setSelectedDate(date)}
                  className={`
                    aspect-square rounded-lg p-1 md:p-2 text-sm md:text-base font-medium
                    transition-smooth relative
                    ${isToday(date) ? 'bg-primary text-primary-foreground' : ''}
                    ${isSelected && !isToday(date) ? 'bg-muted text-foreground' : ''}
                    ${!isSelected && !isToday(date) ? 'text-foreground hover:bg-muted/50' : ''}
                  `}
                >
                  {date?.getDate()}
                  {dayEvents?.length > 0 && (
                    <div className="absolute bottom-1 left-1/2 transform -translate-x-1/2 flex gap-0.5">
                      {dayEvents?.slice(0, 3)?.map((_, i) => (
                        <div key={i} className="w-1 h-1 rounded-full bg-accent"></div>
                      ))}
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        ) : (
          <div className="grid grid-cols-7 gap-1 md:gap-2">
            {dayNames?.map((day) => (
              <div key={day} className="text-center text-xs font-medium text-muted-foreground py-2">
                {day}
              </div>
            ))}
            {Array.from({ length: startingDayOfWeek })?.map((_, index) => (
              <div key={`empty-${index}`} className="aspect-square"></div>
            ))}
            {Array.from({ length: daysInMonth })?.map((_, index) => {
              const date = new Date(year, month, index + 1);
              const dayEvents = getEventsForDate(date);
              const isSelected = date?.getDate() === selectedDate?.getDate() &&
                               date?.getMonth() === selectedDate?.getMonth();
              
              return (
                <button
                  key={index}
                  onClick={() => setSelectedDate(date)}
                  className={`
                    aspect-square rounded-lg p-1 md:p-2 text-sm md:text-base font-medium
                    transition-smooth relative
                    ${isToday(date) ? 'bg-primary text-primary-foreground' : ''}
                    ${isSelected && !isToday(date) ? 'bg-muted text-foreground' : ''}
                    ${!isSelected && !isToday(date) ? 'text-foreground hover:bg-muted/50' : ''}
                  `}
                >
                  {index + 1}
                  {dayEvents?.length > 0 && (
                    <div className="absolute bottom-1 left-1/2 transform -translate-x-1/2 flex gap-0.5">
                      {dayEvents?.slice(0, 3)?.map((_, i) => (
                        <div key={i} className="w-1 h-1 rounded-full bg-accent"></div>
                      ))}
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        )}
      </div>
      <div className="p-4 md:p-6">
        <h3 className="text-sm font-semibold text-foreground mb-3">
          {selectedDateEvents?.length > 0 
            ? `${selectedDateEvents?.length} Release${selectedDateEvents?.length > 1 ? 's' : ''} on ${selectedDate?.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
            : `No releases on ${selectedDate?.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`
          }
        </h3>
        {selectedDateEvents?.length > 0 ? (
          <div className="space-y-3">
            {selectedDateEvents?.map((event) => (
              <CalendarEvent key={event?.id} event={event} />
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Icon name="Calendar" size={48} className="text-muted-foreground mx-auto mb-3 opacity-50" />
            <p className="text-sm text-muted-foreground">No releases scheduled for this date</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default MiniCalendar;